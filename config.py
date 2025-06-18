import os  # Import the operating system module to interact with the file system

# Determine the absolute path of the directory this script is in
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Set the URI for the SQLite database; it will be stored in 'data.db' in the basedir directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SERPAPI_API_KEY = "3f62fef4ad5848514d7e963ac925d6dafd02a1092a91dc3021f35610e2e52834"
    
    # Disable modification tracking to save memory (not necessary for most cases)
    SQLALCHEMY_TRACK_MODIFICATIONS = False