from models.query import Query
from models.router import Router

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