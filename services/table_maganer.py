import pandas as pd
from sqlalchemy import text

from models import db
from models.user import Articles_Keys


def _escape_like(value):
    """Escapa los comodines de LIKE para que se busquen como texto literal."""
    return value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


class Table_Maganer():
  """Consultas de la tabla de artículos (Adquisición).

  Todas las consultas usan parámetros (:profile_id, :title, :year): el texto
  que escribe el usuario nunca se mezcla con el SQL. Los métodos reciben el
  profile_id en cada llamada, así no se comparte estado entre usuarios.
  """

  def __init__(self):
    self.db = db
    self.array_query = ['SELECT title, year FROM Articles WHERE profile_id = :profile_id',
                        'SELECT id_Articles FROM Articles WHERE profile_id = :profile_id']

  def _execute_query(self, profile_id, extra_condition="", params=None):
    params = {"profile_id": profile_id, **(params or {})}
    condition = f" AND {extra_condition}" if extra_condition else ""
    dataframe = pd.read_sql(text(self.array_query[0] + condition), self.db.engine, params=params)
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce').astype('Int64')
    column_articles = pd.read_sql(text(self.array_query[1] + condition), self.db.engine, params=params)
    return dataframe, column_articles

  def get_df_table(self, profile_id):
    return self._execute_query(profile_id)

  def filter_title(self, profile_id, title):
    return self._execute_query(profile_id, "title LIKE :title ESCAPE '\\'",
                               {"title": _escape_like(title) + "%"})

  def filter_year(self, profile_id, year):
    return self._execute_query(profile_id, "year = :year", {"year": int(year)})

  def filter(self, profile_id, title, year):
    return self._execute_query(profile_id, "year = :year AND title LIKE :title ESCAPE '\\'",
                               {"year": int(year), "title": _escape_like(title) + "%"})

  def delete_articles(self, profile_id):
    deleted = Articles_Keys.query.filter_by(profile_id=profile_id).delete(synchronize_session=False)
    db.session.commit()
