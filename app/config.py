import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///DataBase/TESTDB.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
