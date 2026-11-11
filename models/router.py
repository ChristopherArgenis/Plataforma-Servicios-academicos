import pandas as pd

# Clase de Enturamiento
class Router:
    """
    Clase que procesa y organiza la información obtenida de Google Scholar,
    transformándola en estructuras de datos más manejables como diccionarios
    y DataFrames.
    """

    @staticmethod
    def getAuthor(author: dict, cited_by: dict):
        """
        Obtiene las afiliaciones y el número total de citas de un autor.

        Args:
            author (dict): Información general del autor.
            cited_by (dict): Información sobre las citas del autor.

        Returns:
            tuple:
                - str: Afiliaciones del autor.
                - int: Número total de citas.
        """
        affiliations = author["affiliations"]
        cites = cited_by["table"][0]["citas"]["all"]
        return affiliations, cites

    @staticmethod
    def get_pairs(array: list):
        """
        Extrae títulos, identificadores de citas y años de publicación de una lista de artículos.

        Args:
            array (list): Lista de artículos en formato diccionario.

        Returns:
            dict: Diccionario con listas de títulos, IDs de artículos y años.
        """
        title, citation_id, year = [], [], []
        for i in range(len(array)):
            title.append(array[i]["title"])
            citation_id.append(array[i]["citation_id"])
            year.append(array[i]["year"])
        return {"title": title, "id_articles": citation_id, "year": year}

    @staticmethod
    def get_df(array: list, profile_id: str):
        """
        Convierte una lista de artículos en un DataFrame estructurado.

        Args:
            array (list): Lista de artículos en formato diccionario.
            profile_id (str): Identificador del perfil del autor.

        Returns:
            pd.DataFrame: DataFrame con los artículos ordenados por año de forma descendente.
        """
        df = pd.DataFrame(Router.get_pairs(array))
        df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year.astype('Int64')
        df.sort_values(by=['year'], ascending=False, inplace=True)
        df['profile_id'] = profile_id
        return df
    
    @staticmethod
    def schema_citation(clave: str, article: dict):
        """
        Construye un esquema estructurado con la información principal de un artículo.

        Args:
            clave (str): Identificador único asignado al artículo.
            article (dict): Información del artículo en formato diccionario.

        Returns:
            dict: Diccionario con los campos principales del artículo.
        """
        # Safely get publication date
        pub_date = article.get('publication_date')
        if pub_date:
            try:
                date = int(str(pub_date)[:4])
            except (ValueError, TypeError):
                date = 0
        else:
            date = 0

        article_schema = {
            "id_Articles": clave,
            "title": article.get('title', 'Sin título'),
            "authors": article.get('authors', ''),
            "journal": article.get('journal', ''),
            "volume": article.get('volume', 0), # Volume can be int or string, safe 0? Or None? Model has Integer.
            # If model expects Integer for volume, we should be careful. 
            # Looking at models/user.py: volume = db.Column(db.Integer, nullable=True)
            # scholarly might return '12(3)' or valid int. Best to try parse or leave None?
            # Let's use None if missing so SQL handles it.
            "pages": article.get('pages', ''),
            "year": date
        }
        
        # Safe cast for volume if present
        vol = article.get('volume')
        if vol:
            try:
                # If it's a string like "12", int works. If "12(3)", int fails.
                # If db model is Integer, we must ensure it's int or None.
                # Simplest fix for now: try int, else None.
                article_schema["volume"] = int(vol)
            except:
                article_schema["volume"] = None
        else:
             article_schema["volume"] = None
             
        return article_schema