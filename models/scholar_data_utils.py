import pandas as pd

# Clase de Enturamiento
class ScholarDataUtils:

    @staticmethod
    def get_profile(profile):
        perfil = []
        data_require = ["author_id", "affiliations", "cited_by"]
        for i in data_require:
            perfil.append(profile[0][i])
        return perfil

    @staticmethod
    def get_pairs(array):
        title, citation_id, year = [], [], []
        for i in range(len(array)):
            title.append(array[i]["title"])
            citation_id.append(array[i]["citation_id"])
            year.append(array[i]["year"])
        return {"title": title, "id_Articles": citation_id, "year": year}

    @staticmethod
    def get_df(array, profile_id):
        df = pd.DataFrame(ScholarDataUtils.get_pairs(array))
        df['year'] = pd.to_numeric(df['year'])
        df['profile_id'] = profile_id
        return df