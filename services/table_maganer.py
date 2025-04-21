import pandas as pd

class Table_Maganer():
  def __init__(self, db):
    self.db = db
    self.array_query = ['SELECT title, year FROM Articles WHERE profile_id']

  def get_df_table(self, profile_id):
    dataframe = pd.read_sql(f'{self.array_query[0]} == "{profile_id}"', self.db.engine)
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce').astype('Int64')
    return dataframe