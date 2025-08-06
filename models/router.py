import pandas as pd

# Clase de Enturamiento
class Router:
    @staticmethod
    def getAuthor(author, cited_by):
        affiliations = author["affiliations"]
        cites = cited_by["table"][0]["citas"]["all"]
        return affiliations, cites

    @staticmethod
    def get_pairs(array):
        title, citation_id, year = [], [], []
        for i in range(len(array)):
            title.append(array[i]["title"])
            citation_id.append(array[i]["citation_id"])
            year.append(array[i]["year"])
        return {"title": title, "id_articles": citation_id, "year": year}

    @staticmethod
    def get_df(array, profile_id):
        df = pd.DataFrame(Router.get_pairs(array))
        df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year.astype('Int64')
        df.sort_values(by=['year'], ascending=False, inplace=True)
        df['profile_id'] = profile_id
        return df
    
    @staticmethod
    def schema_citation(clave, article):
        if article['publication_date'] == None: 
            date = 0
        else: 
            date = int(article['publication_date'][:4])

        article_schema = {
            "id_Articles": clave,
            "title": article['title'],
            "authors": article['authors'],
            "journal": article['journal'],
            "volume": article['volume'],
            "pages": article['pages'],
            "year": date
        }
        return article_schema