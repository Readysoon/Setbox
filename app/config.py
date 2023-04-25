from os import environ
from dotenv import load_dotenv



class Config:
    def __init__(self, database_url=None, testing=None):
        load_dotenv()

        self.SQLALCHEMY_DATABASE_URI = database_url or environ.get("DATABASE_URL")
        self.TESTING = testing or False
        self.SECRET_KEY = environ.get("SECRET_KEY")
