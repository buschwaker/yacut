import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'Akroshko_1995')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
