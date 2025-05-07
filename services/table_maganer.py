import pandas as pd
from models import db

class Table_Maganer():
  def __init__(self):
    self.db = db
    self.array_query = ['SELECT title, year FROM Articles WHERE profile_id',
                        'SELECT id_Articles FROM Articles WHERE profile_id']

  def get_df_table(self, profile_id):
    self.profile_id = profile_id
    dataframe = pd.read_sql(f'{self.array_query[0]} == "{profile_id}"', self.db.engine)
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce').astype('Int64')
    column_articles = pd.read_sql(f'{self.array_query[1]} == "{profile_id}"', self.db.engine)
    return dataframe, column_articles
  
  def filter_title(self, title):
    dataframe_f = pd.read_sql(f'{self.array_query[0]} == "{self.profile_id}" AND title LIKE "{title}%"', self.db.engine)
    dataframe_f['year'] = pd.to_numeric(dataframe_f['year'], errors='coerce').astype('Int64')
    column_articles_f = pd.read_sql(f'{self.array_query[1]} == "{self.profile_id}" AND title LIKE "{title}%"', self.db.engine)
    return dataframe_f, column_articles_f
  
  def filter_year(self, year):
    dataframe_f = pd.read_sql(f'{self.array_query[0]} == "{self.profile_id}" AND year == {year}', self.db.engine)
    dataframe_f['year'] = pd.to_numeric(dataframe_f['year'], errors='coerce').astype('Int64')
    column_articles_f = pd.read_sql(f'{self.array_query[1]} == "{self.profile_id}" AND year == {year}', self.db.engine)
    return dataframe_f, column_articles_f
  
  def filter(self, title, year):
    dataframe_f = pd.read_sql(f'{self.array_query[0]} == "{self.profile_id}" AND year == {year} AND title LIKE "{title}%"', self.db.engine)
    dataframe_f['year'] = pd.to_numeric(dataframe_f['year'], errors='coerce').astype('Int64')
    column_articles_f = pd.read_sql(f'{self.array_query[1]} == "{self.profile_id}" AND year == {year} AND title LIKE "{title}%"', self.db.engine)
    return dataframe_f, column_articles_f