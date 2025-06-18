import pandas as pd
from models import db
from models.user import Article # Import Article model
from sqlalchemy import func # For functions like like

class TableManager():
  def __init__(self):
    # self.db = db # db is imported and can be used directly. No need to store it on self.
    # self.array_query is no longer needed as we use ORM.
    pass

  def _execute_query_to_dataframe(self, query):
    """Helper function to execute a SQLAlchemy query and return a DataFrame."""
    df = pd.read_sql(query.statement, db.session.bind)
    if 'year' in df.columns:
      df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    return df

  def get_df_table(self, profile_id):
    # Query for title, year, and id_Articles together
    query = db.session.query(Article.title, Article.year, Article.id_Articles)\
                      .filter(Article.profile_id == profile_id)

    dataframe = self._execute_query_to_dataframe(query)

    if dataframe.empty:
        # Return an empty DataFrame with expected columns and an empty Series for id_Articles
        # This helps ensure the controller receives structures it can work with (e.g., .values on an empty Series)
        expected_cols = ['title', 'year', 'id_Articles']
        empty_df = pd.DataFrame(columns=expected_cols)
        if 'year' in empty_df.columns: # Apply type conversion even for empty df
            empty_df['year'] = pd.to_numeric(empty_df['year'], errors='coerce').astype('Int64')
        return empty_df, pd.Series(dtype='object', name='id_Articles')

    id_articles_series = dataframe['id_Articles']
    # Return the main dataframe (potentially without id_Articles if it's only needed as a series)
    # For now, keep it in, controller might use it or ignore.
    return dataframe, id_articles_series

  def filter_title(self, profile_id, title):
    query = db.session.query(Article.title, Article.year, Article.id_Articles)\
                      .filter(Article.profile_id == profile_id, Article.title.like(f"{title}%"))
    dataframe = self._execute_query_to_dataframe(query)
    if dataframe.empty:
        expected_cols = ['title', 'year', 'id_Articles']
        empty_df = pd.DataFrame(columns=expected_cols)
        if 'year' in empty_df.columns:
            empty_df['year'] = pd.to_numeric(empty_df['year'], errors='coerce').astype('Int64')
        return empty_df, pd.Series(dtype='object', name='id_Articles')
    return dataframe, dataframe['id_Articles']

  def filter_year(self, profile_id, year):
    query = db.session.query(Article.title, Article.year, Article.id_Articles)\
                      .filter(Article.profile_id == profile_id, Article.year == year)
    dataframe = self._execute_query_to_dataframe(query)
    if dataframe.empty:
        expected_cols = ['title', 'year', 'id_Articles']
        empty_df = pd.DataFrame(columns=expected_cols)
        if 'year' in empty_df.columns:
            empty_df['year'] = pd.to_numeric(empty_df['year'], errors='coerce').astype('Int64')
        return empty_df, pd.Series(dtype='object', name='id_Articles')
    return dataframe, dataframe['id_Articles']

  def filter(self, profile_id, title, year):
    query = db.session.query(Article.title, Article.year, Article.id_Articles)\
                      .filter(Article.profile_id == profile_id,
                              Article.title.like(f"{title}%"),
                              Article.year == year)
    dataframe = self._execute_query_to_dataframe(query)
    if dataframe.empty:
        expected_cols = ['title', 'year', 'id_Articles']
        empty_df = pd.DataFrame(columns=expected_cols)
        if 'year' in empty_df.columns:
            empty_df['year'] = pd.to_numeric(empty_df['year'], errors='coerce').astype('Int64')
        return empty_df, pd.Series(dtype='object', name='id_Articles')
    return dataframe, dataframe['id_Articles']
