import os

basedir = os.path.abspath(os.path.dirname(__file__))

databaseurl = os.environ.get("DATABASE_URL")

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = f"anysecretkey"
    SQLALCHEMY_DATABASE_URI = databaseurl
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = databaseurl


class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SECRET_KEY = f"anysecretkey"


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'test_app.db')
    WTF_CSRF_ENABLED = False

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test':TestConfig
}




