from flask import Flask
from flask_cors import CORS


def create_app(app_name='PORTAL'):
    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')

    DEBUG = True
    CORS(app, resources={r'/*': {'origins': '*'}})

    from .api import api
    app.register_blueprint(api, url_prefix="/api")

    from .models import db
    db.init_app(app)

    return app
