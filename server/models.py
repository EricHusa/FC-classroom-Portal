from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON  # for if we need to store a json object in the DB
from werkzeug.security import generate_password_hash, check_password_hash
# from app import db
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # role = db.relationship('Role', backref="assignment", lazy=False)

    # hash the password upon instantiating a new User object
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<label {}>'.format(self.label)

    def to_dict(self):
        return dict(id=self.id,
                    name=self.label
                    )


class Example(db.Model):
    __tablename__ = 'sample'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<label {}>'.format(self.text)

    def to_dict(self):
        return dict(id=self.id,
                    text=self.text
                    )