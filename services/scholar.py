"""Consulta de perfiles y artículos de Google Scholar.

Hay dos proveedores con la misma interfaz:
- SerpApiScholar: consulta real a SerpAPI (requiere SERPAPI_KEY).
- DemoScholar: datos inventados, sin internet ni costo (para pruebas y demos).
"""
import hashlib
import random
from dataclasses import dataclass, field

import requests
from flask import current_app

SERPAPI_URL = "https://serpapi.com/search.json"
PAGE_SIZE = 100
MAX_PAGES = 20  # Tope de seguridad: 2,000 artículos


class ScholarError(Exception):
    """Error al consultar Google Scholar (mensaje apto para mostrar al usuario)."""


@dataclass
class Profile:
    author_id: str
    name: str
    affiliations: str = ""
    cited_by: int = 0
    interests: list = field(default_factory=list)


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_article(raw):
    """Convierte un artículo de SerpAPI a dict; devuelve None si no es usable."""
    citation_id = raw.get("citation_id")
    title = (raw.get("title") or "").strip()
    if not citation_id or not title:
        return None
    cited = raw.get("cited_by")
    cited_value = cited.get("value") if isinstance(cited, dict) else cited
    return {
        "citation_id": citation_id,
        "title": title,
        "authors": raw.get("authors") or "",
        "publication": raw.get("publication") or "",
        "year": _to_int(raw.get("year")),
        "cited_by": _to_int(cited_value) or 0,
        "link": raw.get("link") or "",
    }


class SerpApiScholar:
    def __init__(self, api_key, timeout=20):
        if not api_key:
            raise ScholarError("Falta configurar SERPAPI_KEY en el servidor.")
        self.api_key = api_key
        self.timeout = timeout

    def _get(self, params):
        params = {**params, "api_key": self.api_key}
        try:
            resp = requests.get(SERPAPI_URL, params=params, timeout=self.timeout)
            data = resp.json()
        except (requests.RequestException, ValueError) as exc:
            raise ScholarError("No se pudo contactar a Google Scholar. Intenta más tarde.") from exc
        if "error" in data:
            # Sin resultados no es un fallo del servicio
            if "hasn't returned any results" in data["error"]:
                return {}
            current_app.logger.error("SerpAPI: %s", data["error"])
            raise ScholarError("El servicio de Google Scholar devolvió un error.")
        return data

    def search_profiles(self, name):
        data = self._get({"engine": "google_scholar_profiles", "mauthors": name})
        return [
            Profile(
                author_id=p["author_id"],
                name=p.get("name", ""),
                affiliations=p.get("affiliations", ""),
                cited_by=_to_int(p.get("cited_by")) or 0,
                interests=[i.get("title", "") for i in p.get("interests", [])],
            )
            for p in data.get("profiles", [])
            if p.get("author_id")
        ]

    def get_articles(self, author_id):
        articles = []
        for page in range(MAX_PAGES):
            data = self._get({
                "engine": "google_scholar_author",
                "author_id": author_id,
                "start": page * PAGE_SIZE,
                "num": PAGE_SIZE,
            })
            batch = data.get("articles", [])
            articles.extend(a for a in map(parse_article, batch) if a)
            if len(batch) < PAGE_SIZE:
                break
        return articles


# ---------------------------------------------------------------- Demo

_TOPICS = [
    "aprendizaje profundo", "redes neuronales convolucionales", "visión por computadora",
    "procesamiento de lenguaje natural", "sistemas de recomendación", "Internet de las cosas",
    "ciberseguridad", "computación en la nube", "análisis de datos educativos",
    "energías renovables", "redes inalámbricas de sensores", "robótica móvil",
]
_FORMS = [
    "Un enfoque basado en {t} para la detección temprana de fallas",
    "Análisis comparativo de modelos de {t} en entornos universitarios",
    "Aplicación de {t} al monitoreo de calidad del agua",
    "Evaluación de {t} para la clasificación de imágenes médicas",
    "Optimización de recursos mediante {t}: un caso de estudio",
    "Revisión sistemática sobre {t} en América Latina",
    "Diseño e implementación de una plataforma de {t}",
    "Impacto de {t} en el rendimiento académico de estudiantes",
    "Modelo híbrido de {t} para la predicción de demanda energética",
    "Retos y oportunidades de {t} en la industria maquiladora",
]
_VENUES = [
    "Revista Mexicana de Ingeniería", "IEEE Latin America Transactions",
    "Computación y Sistemas", "Congreso Internacional de Ingeniería UABC",
    "Applied Sciences", "Sensors", "Ingeniería, Investigación y Tecnología",
    "Revista Electrónica de Investigación Educativa",
]
_COAUTHORS = ["M. García", "L. Hernández", "R. Martínez", "A. Torres", "S. Ramírez", "J. Castro"]
_AFFILIATIONS = [
    "Universidad Autónoma de Baja California", "Facultad de Ingeniería, UABC",
    "Instituto Tecnológico de Tijuana",
]


def _rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16))


class DemoScholar:
    """Genera perfiles y artículos verosímiles a partir del nombre (siempre iguales)."""

    def search_profiles(self, name):
        name = name.strip()
        if not name:
            return []
        rng = _rng(name)
        return [
            Profile(
                author_id=f"DEMO{hashlib.sha1(f'{name}{i}'.encode()).hexdigest()[:8].upper()}",
                name=name if i == 0 else f"{name} {rng.choice(['A.', 'M.', 'R.'])}",
                affiliations=_AFFILIATIONS[i % len(_AFFILIATIONS)],
                cited_by=rng.randint(20, 2500),
                interests=rng.sample(_TOPICS, 3),
            )
            for i in range(rng.randint(1, 3))
        ]

    def get_articles(self, author_id):
        rng = _rng(author_id)
        articles = []
        for i in range(rng.randint(25, 60)):
            title = rng.choice(_FORMS).format(t=rng.choice(_TOPICS))
            title = title[0].upper() + title[1:]
            year = rng.randint(2010, 2025) if rng.random() > 0.05 else None
            articles.append({
                "citation_id": f"{author_id}:{i:04d}",
                "title": title,
                "authors": ", ".join(rng.sample(_COAUTHORS, rng.randint(1, 4))),
                "publication": f"{rng.choice(_VENUES)}" + (f", {year}" if year else ""),
                "year": year,
                "cited_by": int(rng.expovariate(1 / 15)),
                "link": "",
            })
        return articles


def get_scholar_client():
    """Devuelve el proveedor configurado en SCHOLAR_PROVIDER."""
    if current_app.config["SCHOLAR_PROVIDER"] == "demo":
        return DemoScholar()
    return SerpApiScholar(current_app.config["SERPAPI_KEY"])
