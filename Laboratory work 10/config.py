import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = f"anysecretkey"
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'app.db')


class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'app.db')


    
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}