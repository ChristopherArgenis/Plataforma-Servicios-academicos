# pip install serpapi google-search-results
# Bibliotecas Necesarias
from serpapi import GoogleSearch
import pandas as pd
# import json

# Clase de Consulta
class Query:
    api_key = "17f3094e233931a4b2d2d2a0fb5f957c0dfd63af173422a6ae794fd50266b222"
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
    
# Clase de Enturamiento
class Router:

    @staticmethod
    def get_profile(profile):
        perfil = []
        data_require = ["author_id", "affiliations", "cited_by"]
        for i in data_require:
            perfil.append(profile[0][i])
        return perfil

    @staticmethod
    def get_pairs(array):
        title, citation_id, year = [], [], []
        for i in range(len(array)):
            title.append(array[i]["title"])
            citation_id.append(array[i]["citation_id"])
            year.append(array[i]["year"])
        return {"title": title, "id_Articles": citation_id, "year": year}

    @staticmethod
    def get_df(array, profile_id):
        df = pd.DataFrame(Router.get_pairs(array))
        df['year'] = pd.to_numeric(df['year'])
        df['profile_id'] = profile_id
        return df
    
# Manejador de Consultas
class Query_Manager:
  def __init__(self, Name):
    # Datos Iniciales
    self.name = Name
    self.query = Query() # Class Static
    self.router = Router() # Class Static
    # Datos Consultados
    self.Author_Dict = self.query.authors(self.name)
    # Datos Procesados
    self.profile_id = self.get_profile_id()
    # Datos Consultados
    self.Article_Array = self.get_articles()

  # DataBase -> User's Table
  def get_profile_data(self):
    return self.router.get_profile(self.Author_Dict) # List

  def get_profile_id(self):
    return self.get_profile_data()[0] # String

  def get_articles(self):
    return self.query.articles(self.profile_id) # Array

  # DataBase -> Article's Table
  def get_dataframe(self):
    return self.router.get_df(self.Article_Array, self.profile_id) # DataFrame