"""Validación y guardado de la firma del reporte.

La firma llega dibujada en el navegador (data URL PNG) o como imagen subida
(PNG, JPG o WEBP, por ejemplo una firma escaneada). En ambos casos se
normaliza: fondo claro -> transparente, recorte a la tinta y tamaño acotado.
"""
import base64
import binascii
import io

from PIL import Image, UnidentifiedImageError

from extensions import db
from models import ReportSignature

MAX_BYTES = 1024 * 1024          # 1 MB por firma
MAX_PIXELS = 4000 * 4000         # evita imágenes "bomba"
OUTPUT_SIZE = (900, 300)         # tamaño máximo guardado
ALLOWED_FORMATS = {"PNG", "JPEG", "WEBP"}
LIGHT_THRESHOLD = 225            # más claro que esto se considera fondo
DATA_URL_PREFIX = "data:image/png;base64,"


class SignatureError(Exception):
    """Firma inválida (mensaje apto para mostrar al usuario)."""


def decode_data_url(data_url):
    if not data_url.startswith(DATA_URL_PREFIX):
        raise SignatureError("Formato de firma no válido.")
    try:
        raw = base64.b64decode(data_url[len(DATA_URL_PREFIX):], validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SignatureError("Formato de firma no válido.") from exc
    return raw


def normalize(raw):
    """Devuelve un PNG con fondo transparente recortado a la firma."""
    if not raw:
        raise SignatureError("Dibuja o sube tu firma.")
    if len(raw) > MAX_BYTES:
        raise SignatureError("La imagen de la firma pesa más de 1 MB.")
    try:
        img = Image.open(io.BytesIO(raw))
        if img.format not in ALLOWED_FORMATS:
            raise SignatureError("La firma debe ser PNG, JPG o WEBP.")
        if img.width * img.height > MAX_PIXELS:
            raise SignatureError("La imagen de la firma es demasiado grande.")
        img.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise SignatureError("No se pudo leer la imagen de la firma.") from exc

    img = img.convert("RGBA")
    # Pixeles claros (papel, fondo blanco) o ya transparentes -> transparentes
    gray = img.convert("L")
    mask = gray.point(lambda v: 255 if v < LIGHT_THRESHOLD else 0)
    alpha = Image.composite(img.getchannel("A"), Image.new("L", img.size, 0), mask)
    img.putalpha(alpha)

    box = alpha.getbbox()
    if not box:
        raise SignatureError("La firma está vacía. Dibuja o sube tu firma.")
    pad = 8
    box = (max(box[0] - pad, 0), max(box[1] - pad, 0),
           min(box[2] + pad, img.width), min(box[3] + pad, img.height))
    img = img.crop(box)
    img.thumbnail(OUTPUT_SIZE)

    out = io.BytesIO()
    img.save(out, format="PNG", optimize=True)
    return out.getvalue()


def save(user, signer_name, signer_title, image_png=None):
    """Crea o actualiza la firma. Sin imagen nueva solo cambia nombre y cargo."""
    sig = user.signature
    if sig is None:
        if image_png is None:
            raise SignatureError("Dibuja o sube tu firma.")
        sig = ReportSignature(user=user, image=image_png,
                              signer_name=signer_name, signer_title=signer_title)
        db.session.add(sig)
    else:
        if image_png is not None:
            sig.image = image_png
        sig.signer_name = signer_name
        sig.signer_title = signer_title
    db.session.commit()
    return sig


def delete(user):
    if user.signature is not None:
        db.session.delete(user.signature)
        db.session.commit()
