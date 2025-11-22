import pandas as pd
from models import db
from models.user import Articles_Keys

import pandas as pd
from models import db
from models.user import Articles_Keys

class Table_Maganer():
  def __init__(self):
    self.db = db
    self.array_query = ['SELECT title, year FROM Articles WHERE profile_id',
                        'SELECT id_Articles FROM Articles WHERE profile_id']

  def _execute_query(self, extra_condition=""):
    base_condition = f' == "{self.profile_id}"'
    if extra_condition:
        base_condition += f' AND {extra_condition}'
    
    dataframe = pd.read_sql(f'{self.array_query[0]}{base_condition}', self.db.engine)
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce').astype('Int64')
    column_articles = pd.read_sql(f'{self.array_query[1]}{base_condition}', self.db.engine)
    return dataframe, column_articles

  def get_df_table(self, profile_id):
    self.profile_id = profile_id
    return self._execute_query()
  
  def filter_title(self, title):
    return self._execute_query(f'title LIKE "{title}%"')
  
  def filter_year(self, year):
    return self._execute_query(f'year == {year}')
  
  def filter(self, title, year):
    return self._execute_query(f'year == {year} AND title LIKE "{title}%"')
  
  def delete_articles(self, profile_id):
    deleted = Articles_Keys.query.filter_by(profile_id=profile_id).delete(synchronize_session=False)
    db.session.commit()