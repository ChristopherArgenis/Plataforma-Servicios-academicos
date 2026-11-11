from models.query import Query
from models.router import Router

# Manejador de Consultas
class Query_Manager:
  def __init__(self, clave):
    # Datos Iniciales
    self.profile_id = clave
    self.query = Query() # Class Static
    self.router = Router() # Class Static
    # Datos Consultados
    self.Author_Dict = self.query.authors(self.profile_id) # Two Variable
    self.Article_Array = self.get_articles()

  # DataBase -> User's Table
  def get_profile_data(self):
    return self.router.getAuthor(author=self.Author_Dict[0], cited_by=self.Author_Dict[1]) # List

  def get_articles(self):
    return self.query.articles(self.profile_id) # Array

  # DataBase -> Article's Table
  def get_dataframe(self):
    return self.router.get_df(self.Article_Array, self.profile_id) # DataFrame