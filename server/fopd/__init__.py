from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
#from flask_migrate import Migrate

from fopd.config import Config

# use same object with different apps
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
#migrate = Migrate()

def create_app(config_object = Config):
    app = Flask(__name__)
    app.config.from_object(config_object) # flask app configuration in config.py

    # initialize object
    db.init_app(app)
    #migrate.init_app(app, db)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)

    from fopd.routes.school import schools
    from fopd.routes.teacher import teachers
    from fopd.routes.admin import admins
    # from fopd.routes.student import students
    # from fopd.routes.experiment import experiments
    # from fopd.routes.course import courses
    # from fopd.routes.assignment import assignments
    # from fopd.routes.assignment_resp import assignment_responses
    # from fopd.routes.observation import observations
    # from fopd.routes.observation_resp import observation_responses
    # from fopd.routes.measurement import measurements
    # from fopd.routes.measurement_resp import measurement_responses
    # from fopd.routes.device import devices
    # from fopd.routes.external import externals

    app.register_blueprint(schools)
    app.register_blueprint(teachers)
    app.register_blueprint(admins)
    # app.register_blueprint(students)
    # app.register_blueprint(experiments)
    # app.register_blueprint(courses)
    # app.register_blueprint(assignments)
    # app.register_blueprint(assignment_responses)
    # app.register_blueprint(observations)
    # app.register_blueprint(observation_responses)
    # app.register_blueprint(measurements)
    # app.register_blueprint(measurement_responses)
    # app.register_blueprint(devices)
    # app.register_blueprint(externals)

    return app

