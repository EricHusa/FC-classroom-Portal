from flask import Blueprint, request, jsonify

from fopd import db, bcrypt
# from fopd.models import Student, Teacher
from fopd.models import Student, Course
from sqlalchemy import and_

import uuid, datetime

students = Blueprint('students', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200
MIN_PASSWORD_LENGTH = 6


'''
Get a list of all Students belonging to a School.

url parameter:
* school_id - School abbreviation

output:
* message - execution result message
* students - list of serialized Student accounts
'''
@students.route('/api/schools/<school_id>/students', methods = ['GET'])
def get_students_by_school(school_id):
    # Request checks
    school = School.query.filter_by(abbreviation = school_id).first()

    if not school:
        return jsonify({
            'message': 'School not found'
        }), ERROR_CODE
    
    # Return result
    output = school.serialized_students()
    message = str(len(output)) + ' students found'
    return jsonify({
        'message': message,
        'students': output
    }), SUCCESS_CODE



'''
Get a list of all Students belonging to a certain Class.

url parameter:
* teacher_id - id of Teacher who created the class
* class_id - Unique Class id

output:
* message - execution result message
* students - list of serialized Student accounts
'''
@students.route('/api/teachers/<teacher_id>/classes/<class_id>/students', methods = ['GET'])
def get_students_by_class(class_id):
    # Request checks
    class_ = Course.query.filter_by(id = class_id).first()

    if not class_:
        return jsonify({
            'message': 'Class not found'
        }), ERROR_CODE
    
    # Return result
    output = class_.serialized_students()
    message = str(len(output)) + ' students found'
    return jsonify({
        'message': message,
        'students': output
    }), SUCCESS_CODE


'''
Get a student account.

url parameter:
* student_id - Unique class id

output:
* message - execution result message
* students - list of serialized Student accounts
'''
@students.route('/api/students/<student_id>', methods = ['GET'])
def get_student_by_id(student_id):
    # Request checks
    student = Student.query.filter_by(id = student_id).first()
    
    if not student:
        return jsonify({
            'message': f'Account id `{student_id}` does not exist',
            'student': {}
        }), ERROR_CODE

    # Return result
    output = student.serialized_students()
    return jsonify({
        'message': 'success',
        'students': output
    }), SUCCESS_CODE


'''
Create a Student account

url parameter:
* school_id - Student's School abbreviation

required request parameters:
* username
* display_name
* password

optional request parameters:
* fname
* lname

output:
* message - execution result message
* teacher - serialized newly created Teacher account
'''
@students.route('/auth/register/schools/<school_id>/students', methods = ['POST'])
def register_student_account():
    # Request checks
    account_info = request.json
    school = School.query.filter_by(abbreviation = school_id).first()

    if not school:
        return jsonify({
            'message': 'School not found'
        }), ERROR_CODE

    if not account_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE

    parameters = {}
    parameter['username'] = account_info.get('username', None)
    parameter['password'] = account_info.get('password', None)
    parameter['display_name'] = account_info.get('display_name', None)
    parameter['fname'] = account_info.get('fname', None)
    parameter['lname'] = account_info.get('lname', None)
    parameter['id'] = str(uuid.uuid4())

    # Verify uniqueness for school
    existing_student = Student.query.filter(and_(username == user, school == school_id)).first()
    if existing_student:
        return jsonify({
            'message': 'Username already in use'
        }), ERROR_CODE

    student = Student()
    for p in parameters:
        if parameters[p]:
            student[p] = parameters[p]


    # Commit to datbase
    try:
        output = student.serialize()
        db.session.add(student)
        db.session.commit()
        return jsonify({
            'message': 'Successfully created',
            'student': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create account',
            'student': {}
        }), ERROR_CODE


'''
Login as a Student

url parameter:
* school_id - Teacher's School abbreviation

required request parameters:
* username
* password

output:
* message - execution result message
* student - serialized logged in Student account
'''
@students.route('/auth/schools/<school_id>/students/login', methods = ['POST'])
def student_login():
    # Request checks
    credentials = request.json

    if not credentials:
        return jsonify({
            'message': 'No login credentials provided'
        }), ERROR_CODE

    username = credentials.get('username', '')
    password = credentials.get('password', '')
    if not password or not username:
        return jsonify({
            'message': 'No username or password provided'
        }), ERROR_CODE
    
    student = Student.query.filter(and_(school == school_id, username == username)).first()

    if not student:
        return jsonify({
            'message': f'Invalid username `{username}`'
        }), ERROR_CODE

    # Return results
    encoded_password = password.encode('utf-8')
    if student.password == password: 
        output = student.serialize()
        return jsonify({
            'message': 'Logged in',
            'token': str(uuid.uuid1()),
            'student': output
        }), SUCCESS_CODE

    return jsonify({
            'message': f'Invalid password'
        }), ERROR_CODE


'''
Update a Student's account information.

url parameter:
* student - Student id

available request parameters:
* username
* password
* fname
* lname
* display_name

output:
* message - execution result message
* student - serialized updated Student object
'''
@students.route('/api/schools/<school_id>/students/<student_id>', methods = ['PUT'])
def update_student_account(student_id):
    # Request checks
    update_info = request.json

    # Request checks
    if not update_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE

    student = Student.query.filter_by(id == student_id).first()
    if not student:
        return jsonify({
            'message': f'Invalid username `{username}`'
        }), ERROR_CODE


    # Value checks
    user = update_info.get('username', None)
    if user and student.username != user:
        student.username = user

        existing_student = Student.query.filter(and_(username == user, school == school_id)).first()
        if existing_student:
            return jsonify({
                'message': 'Username already in use'
            }), ERROR_CODE

    pw = update_info.get('password', student.password)
    if pw and student.password != pw:
        if len(pw < MIN_PASSWORD_LENGTH):
            return jsonify({
                'message': 'Password must be ' + str(MIN_PASSWORD_LENGTH) + ' characters in length'
            }), ERROR_CODE

        student.password = pw

    student.fname = update_info.get('fname', student.fname)
    student.lname = update_info.get('lname', student.lname)
    student.display_name = update_info.get('display_name', student.display_name)


    # Commit to database
    try:
        output = student.serialize()
        db.session.add(student)
        db.session.commit()
        return jsonify({
            'message': 'Account updated',
            'student': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update account'
        }), ERROR_CODE



'''
Delete a Student account

url parameter:
* student_id - Student's primary id

output:
* message - execution result message
'''
@students.route('/api/students/<student_id>', methods = ['DELETE'])
def delete_student_account(student_id):
    # Request checks
    """delete student account by id"""
    student = Student.query.filter_by(public_id = student_id).first()

    if not student:
        return jsonify({
            'message': f'Account id: `{student_id}` does not exist'
        }), ERROR_CODE

    # Commit to datbase
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({
            'message': f'Account id: `{student_id}` has been deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete account
        }), ERROR_CODE

