import os


class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'DATABASE_URL'       # os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = 'mysecretkey'
