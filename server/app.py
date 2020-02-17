import os
from flask import Flask
from flask_cors import CORS
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.BaseConfig')  # or app.config.from_object(os.environ['APP_SETTINGS'])

from models import db
db.init_app(app)

#db = SQLAlchemy(app)
from api import api

DEBUG = True
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run()


# Older method, keep for now
# def create_app(app_name='PORTAL'):
#     app = Flask(__name__)
#     app.config.from_object('config.BaseConfig')  # or app.config.from_object(os.environ['APP_SETTINGS'])
#
#     DEBUG = True
#     CORS(app, resources={r'/*': {'origins': '*'}})
#
#     from .api import api
#     app.register_blueprint(api, url_prefix="/api")
#
#     db = SQLAlchemy(app)
#
#     return app
