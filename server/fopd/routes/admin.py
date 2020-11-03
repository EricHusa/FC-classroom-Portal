from flask import Blueprint, request, jsonify

from fopd import db, bcrypt
from fopd.models import Teacher, School

import uuid

admins = Blueprint('admins', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200

@admins.route('/admin/delete_all', methods = ['POST'])
def register_teacher_account():
    try:
        Teacher.query.delete()
        School.query.delete()

        db.session.commit()
    except:
        return jsonify({
            'message': 'Cannot clear database'
        }), ERROR_CODE

    return jsonify({
            'message': 'Database cleared'
        }), SUCCESS_CODE
