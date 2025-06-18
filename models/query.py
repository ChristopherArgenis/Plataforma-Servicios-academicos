from serpapi import GoogleSearch
from flask import current_app

# Clase de Consulta
class Query:
    engine = "google_scholar_author"

    @staticmethod
    def get_dict(type: str, params: dict):
        search = GoogleSearch(params)
        results = search.get_dict()
        return results[type]

    @staticmethod
    def authors(author):
        params = {
            "engine": "google_scholar_profiles",
            "mauthors": author,
            "api_key": current_app.config['SERPAPI_API_KEY']
        }
        profile = Query.get_dict("profiles", params)
        return profile

    @staticmethod
    def articles(author_id):
      all_articles = []
      start = 0
      while True:
        params = {
            "engine": Query.engine,
            "author_id": author_id,
            "api_key": current_app.config['SERPAPI_API_KEY'],
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
    def article(citation_id):
        params = {
            "engine": Query.engine,
            "view_op": "view_citation",
            "citation_id": citation_id,
            "api_key": current_app.config['SERPAPI_API_KEY']
        }
        article = Query.get_dict("citation", params)
        return article