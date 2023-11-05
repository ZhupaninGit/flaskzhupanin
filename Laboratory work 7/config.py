from os import path as pt

basedir = pt.abspath(pt.dirname(__file__))

#General Config
WTF_CSRF_ENABLED = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

#Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False