import os
from datetime import timedelta

class Config(object):
    DEBUG= False
    TESTING= False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY= "1fegrsgfhtyrnfdghk784hfuue"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


    #app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI") 
    #DB_NAME= "production-db"
    #DB_USERNAME= 'postgres'
    #DB_PASSWORD ="tamar"
    #path to upload image on development server
    #UPLOADS= '/home/username/app/static/images/uploads'

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG= True

    #UPLOADS= '/home/username/projects/flask_testapp/static/images/uploads'
    SQLALCHEMY_ECHO = False
    JSON_SORT_KEYS = False
    JWT_ACCESS_TOKEN_EXPIRES = False #timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_CREATE_TOKEN_EXPIRES = False #timedelta(minutes=20)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING= True

    SQLALCHEMY_ECHO = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(basedir, "../mytest.sqlite")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    #SQLALCHEMY_DATABASE_URI = get_env('TEST_DB')
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_CSRF_IN_COOKIES = False
    JWT_ACCESS_CSRF_HEADER_NAME = "csrf_token"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

    SESSION_COOKIE_SECURE = False



settings = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}