from flask import Blueprint, jsonify, request, current_app
from functools import wraps
from datetime import datetime, timedelta
import jwt

from .models import db, User

api = Blueprint('api', __name__)


@api.route('/test/<string:example>/')
def tester(example):
    response = {'msg': "You sent: {}".format(example)}
    return jsonify(response)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Re-authentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@api.route('/register/', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login/', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),  # time the jwt was issued at
        'exp': datetime.utcnow() + timedelta(minutes=30)},  # moment the jwt should expire
        current_app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})


@api.route('/experiments', methods=['GET'])
@token_required
def fetch_experiments():
    return jsonify({
        'status': 'success'
    })
