from flask import current_app
from serpapi import GoogleSearch
from models.scholar_data_utils import ScholarDataUtils # Asegurar que la importación sea correcta

class ScholarAPIClient:
    def __init__(self):
        self.api_key = current_app.config['SERPAPI_API_KEY']
        self.engine_author_profiles = "google_scholar_profiles"
        self.engine_author_articles = "google_scholar_author"

    def _get_serpapi_data(self, params):
        search = GoogleSearch(params)
        return search.get_dict()

    def fetch_author_profile_data(self, author_name):
        params = {
            "engine": self.engine_author_profiles,
            "mauthors": author_name,
            "api_key": self.api_key
        }
        results = self._get_serpapi_data(params)
        return results.get("profiles")

    def fetch_author_articles_data(self, author_id):
        all_articles_raw = []
        start_index = 0
        page_size = 100
        while True:
            params = {
                "engine": self.engine_author_articles,
                "author_id": author_id,
                "api_key": self.api_key,
                "start": start_index,
                "num": page_size
            }
            results = self._get_serpapi_data(params)
            articles_page = results.get("articles")
            if not articles_page:
                break
            all_articles_raw.extend(articles_page)
            if len(articles_page) < page_size:
                break
            start_index += page_size
        return all_articles_raw

class QueryManager:
    def __init__(self):
        self.scholar_api_client = ScholarAPIClient()
        self.scholar_data_utils = ScholarDataUtils()
        # No almacenar author_id como estado de instancia aquí para mantener los métodos más independientes

    def get_profile_data(self, author_name):
        raw_profiles = self.scholar_api_client.fetch_author_profile_data(author_name)
        if not raw_profiles or not isinstance(raw_profiles, list) or not raw_profiles[0]:
            raise ValueError(f"Perfil no encontrado o formato inesperado para {author_name}")

        # Extraer el author_id del primer perfil (necesario para el controlador)
        # La implementación original de ScholarDataUtils.get_profile espera raw_profiles[0]
        # y extrae "author_id", "affiliations", "cited_by". El primer elemento es el author_id.
        # Corregido: ScholarDataUtils.get_profile espera la lista de perfiles directamente.
        processed_profile_list = self.scholar_data_utils.get_profile(raw_profiles)

        if not processed_profile_list or not processed_profile_list[0]:
             raise ValueError(f"No se pudo extraer el author_id del perfil para {author_name}")

        # Devolvemos la lista procesada como antes, donde el primer elemento es el author_id
        return processed_profile_list

    def get_articles_dataframe(self, author_id):
        articles_raw = self.scholar_api_client.fetch_author_articles_data(author_id)
        # fetch_author_articles_data inicializa all_articles_raw = [] y la extiende,
        # por lo que devolverá una lista vacía si no hay artículos, no None.
        # El método get_df de ScholarDataUtils debería poder manejar una lista vacía de artículos.
        return self.scholar_data_utils.get_df(articles_raw, author_id)
