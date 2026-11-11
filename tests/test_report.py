import base64
import io

from PIL import Image, ImageDraw
from pypdf import PdfReader

from extensions import db
from models import Article, ReportSignature, User
from tests.conftest import register


def _signature_png(background=(255, 255, 255, 255), fmt="PNG"):
    img = Image.new("RGBA" if fmt == "PNG" else "RGB", (400, 150), background[:3] if fmt != "PNG" else background)
    ImageDraw.Draw(img).line([(30, 100), (150, 40), (260, 110), (370, 50)], fill=(10, 20, 60), width=6)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def _data_url(png):
    return "data:image/png;base64," + base64.b64encode(png).decode()


def _select_some(app, email="ana@x.com", n=3):
    with app.app_context():
        user = User.query.filter_by(email=email).one()
        arts = user.articles.limit(n).all()
        for a in arts:
            a.selected = True
        db.session.commit()
        return [a.title for a in arts]


def _pdf_text(data):
    return "\n".join(page.extract_text() for page in PdfReader(io.BytesIO(data)).pages)


def test_save_drawn_signature(app, client):
    register(client)
    resp = client.post("/panel/firma", data={"signer_name": "Ana López", "signer_title": "Profesora",
                                             "signature_data": _data_url(_signature_png())})
    assert resp.status_code == 302 and "paso=4" in resp.location
    with app.app_context():
        sig = ReportSignature.query.one()
        assert sig.signer_name == "Ana López" and sig.signer_title == "Profesora"
        img = Image.open(io.BytesIO(sig.image))
        assert img.format == "PNG" and img.mode == "RGBA"
        # El fondo blanco quedó transparente y la imagen se recortó a la tinta
        assert img.getpixel((0, 0))[3] == 0
        assert img.width < 400
    img_resp = client.get("/panel/firma.png")
    assert img_resp.status_code == 200 and img_resp.mimetype == "image/png"


def test_upload_scanned_signature_jpg(app, client):
    register(client)
    jpg = _signature_png(fmt="JPEG")
    resp = client.post("/panel/firma", data={"signer_name": "Ana",
                                             "signature_file": (io.BytesIO(jpg), "firma.jpg")},
                       content_type="multipart/form-data")
    assert "paso=4" in resp.location
    with app.app_context():
        assert ReportSignature.query.count() == 1


def test_invalid_signatures_are_rejected(app, client):
    register(client)
    blank = _signature_png()
    blank_img = Image.new("RGBA", (300, 100), (255, 255, 255, 255))
    buf = io.BytesIO()
    blank_img.save(buf, format="PNG")
    cases = [
        {"signer_name": "Ana", "signature_data": "data:image/png;base64,@@no-es-base64@@"},
        {"signer_name": "Ana", "signature_data": "data:text/html;base64,PGgxPg=="},
        {"signer_name": "Ana", "signature_data": _data_url(buf.getvalue())},   # vacía
        {"signer_name": "Ana", "signature_data": _data_url(b"no es una imagen")},
        {"signer_name": "", "signature_data": _data_url(blank)},             # sin nombre
        {"signer_name": "Ana"},                                              # sin firma
    ]
    for data in cases:
        resp = client.post("/panel/firma", data=data)
        assert "paso=3" in resp.location, data
    with app.app_context():
        assert ReportSignature.query.count() == 0


def test_update_name_keeps_image_and_delete(app, client):
    register(client)
    client.post("/panel/firma", data={"signer_name": "Ana", "signature_data": _data_url(_signature_png())})
    client.post("/panel/firma", data={"signer_name": "Dra. Ana", "signer_title": "Coordinadora"})
    with app.app_context():
        sig = ReportSignature.query.one()
        assert sig.signer_name == "Dra. Ana" and sig.image
    client.post("/panel/firma/borrar")
    with app.app_context():
        assert ReportSignature.query.count() == 0
    assert client.get("/panel/firma.png").status_code == 404


def test_signature_is_private(app, client):
    register(client, name="Ana", email="ana@x.com")
    client.post("/panel/firma", data={"signer_name": "Ana", "signature_data": _data_url(_signature_png())})
    client.post("/logout")
    assert client.get("/panel/firma.png").status_code == 302  # pide login
    register(client, name="Beto", email="beto@x.com")
    assert client.get("/panel/firma.png").status_code == 404  # Beto no tiene firma


def test_pdf_requires_selected_articles(client):
    register(client)
    resp = client.get("/panel/reporte.pdf")
    assert resp.status_code == 302 and "paso=2" in resp.location


def test_pdf_draft_without_signature(app, client):
    register(client)
    titles = _select_some(app)
    resp = client.get("/panel/reporte.pdf")
    assert resp.status_code == 200 and resp.mimetype == "application/pdf"
    assert resp.data.startswith(b"%PDF")
    text = _pdf_text(resp.data)
    assert "BORRADOR" in text and "Reporte de producción académica" in text
    assert all(t.split()[0] in text for t in titles)


def test_pdf_with_signature_and_download(app, client):
    register(client)
    _select_some(app, n=2)
    client.post("/panel/firma", data={"signer_name": "Dra. Ana López", "signer_title": "Investigadora",
                                      "signature_data": _data_url(_signature_png())})
    resp = client.get("/panel/reporte.pdf?descargar=1")
    assert resp.status_code == 200
    assert "attachment" in resp.headers["Content-Disposition"]
    assert ".pdf" in resp.headers["Content-Disposition"]
    text = _pdf_text(resp.data)
    assert "BORRADOR" not in text
    assert "Dra. Ana López" in text and "Investigadora" in text
    assert "Artículos incluidos" in text


def test_pdf_escapes_markup_and_long_lists(app, client):
    register(client)
    with app.app_context():
        user = User.query.one()
        user.articles.update({Article.selected: True})
        art = user.articles.first()
        art.title = 'Título con <b>etiquetas</b> & "símbolos" <script>'
        db.session.commit()
        total = user.articles.count()
    resp = client.get("/panel/reporte.pdf")
    assert resp.status_code == 200
    text = _pdf_text(resp.data)
    assert "<b>etiquetas</b>" in text and "&" in text
    assert str(total) in text
    assert len(PdfReader(io.BytesIO(resp.data)).pages) >= 2  # la tabla continúa en otra página


def test_panel_opens_requested_step(client):
    register(client)
    html = client.get("/panel?paso=3").data.decode()
    assert 'data-initial-step="3"' in html
    assert 'data-initial-step="4"' in client.get("/panel?paso=99").data.decode()


def test_too_large_upload(client):
    register(client)
    big = b"0" * (3 * 1024 * 1024)
    resp = client.post("/panel/firma", data={"signer_name": "Ana", "signature_file": (io.BytesIO(big), "f.png")},
                       content_type="multipart/form-data")
    assert resp.status_code == 413
