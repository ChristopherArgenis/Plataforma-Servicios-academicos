from serpapi import GoogleSearch

# Clase de Consulta
class Query:
    api_key = "3f62fef4ad5848514d7e963ac925d6dafd02a1092a91dc3021f35610e2e52834"
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
            "api_key": Query.api_key
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
    def article(citation_id):
        params = {
            "engine": Query.engine,
            "view_op": "view_citation",
            "citation_id": citation_id,
            "api_key": Query.api_key
        }
        article = Query.get_dict("citation", params)
        return article