from serpapi import GoogleScholarSearch

class Query:
    """
    Clase que gestiona consultas a la API de SerpAPI para Google Scholar.

    Attributes:
        api_key (str): Clave de autenticación para usar la API de SerpAPI.
        engine (str): Motor de búsqueda definido para Google Scholar Author.
    """

    api_key = "3f62fef4ad5848514d7e963ac925d6dafd02a1092a91dc3021f35610e2e52834"
    engine = "google_scholar_author"

    @staticmethod
    def get_dict(types: str, params: dict):
        """
        Realiza una búsqueda en Google Scholar y devuelve un diccionario con los resultados.

        Args:
            types (str): Tipo de información a obtener (por ejemplo: "author", "articles").
            params (dict): Parámetros de la consulta a SerpAPI.

        Returns:
            dict | list: Resultados de la búsqueda en formato diccionario o lista según el tipo.
        """
        search = GoogleScholarSearch(params)
        results = search.get_dict()
        return results[types]

    @staticmethod
    def authors(authorID: str):
        """
        Obtiene información de un autor específico y sus citas en Google Scholar.

        Args:
            authorID (str): Identificador del autor en Google Scholar.

        Returns:
            tuple: 
                - dict: Información general del autor.
                - dict: Información sobre las citas del autor.
        """
        params = {
            "engine": "google_scholar_author",
            "author_id": authorID,
            "api_key": Query.api_key,
            "hl": "es"
        }
        author = Query.get_dict("author", params)
        cited_by = Query.get_dict("cited_by", params)
        return author, cited_by

    @staticmethod
    def articles(author_id: str):
        """
        Recupera todos los artículos asociados a un autor en Google Scholar.

        Args:
            author_id (str): Identificador del autor en Google Scholar.

        Returns:
            list: Lista con los artículos del autor.
        """
        all_articles = []
        start = 0
        while True:
            params = {
                "engine": Query.engine,
                "author_id": author_id,
                "api_key": Query.api_key,
                "start": start,
                "num": 100
            }
            articles = Query.get_dict("articles", params)
            if not articles:
                break
            all_articles.extend(articles)
            if len(articles) < 100:
                break
            start += 100
        return all_articles

    @staticmethod
    def article(citation_id: str):
        """
        Obtiene la información detallada de una cita específica en Google Scholar.

        Args:
            citation_id (str): Identificador de la cita en Google Scholar.

        Returns:
            dict: Información de la cita consultada.
        """
        params = {
            "engine": Query.engine,
            "view_op": "view_citation",
            "citation_id": citation_id,
            "api_key": Query.api_key
        }
        article = Query.get_dict("citation", params)
        return article