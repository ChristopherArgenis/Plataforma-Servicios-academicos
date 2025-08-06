from models.query import Query
from models.router import Router
import pandas as pd

# Manejador de Articulos Completos
class Articles_Maganer:
    def __init__(self):
        # Datos Iniciales
        self.query = Query() # Class Static
        self.router = Router() # Class Static
        self.data = []

    def query_article(self, clave):
        article = self.query.article(clave)
        if isinstance(article, dict):
            clean_article = self.router.schema_citation(clave, article)
            self.data.append(clean_article)

    def iteration_articles(self, array):
        for clave in array:
            self.query_article(clave)
        self.fail = len(array) - len(self.data)
        return self.data

    def df_articles(self, array):
        return pd.DataFrame(self.iteration_articles(array))