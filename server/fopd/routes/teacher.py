from flask import Blueprint, request, jsonify

from fopd import db, bcrypt
from fopd.models import Teacher, School

import uuid

teachers = Blueprint('teachers', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Teachers belonging to a School.

url parameter:
* school_id - School abbreviation

output:
* message - execution result message
* teachers - list of serialized Teacher accounts
'''
@teachers.route('/api/schools/<school_id>/teachers', methods = ['GET'])
def get_school_teachers(school_id):
    # Request processing
    teachers = Teacher.query.filter_by(school = school_id)

    # Format output
    output = [i.serialize() for i in teachers]
    
    # Return results
    message = str(len(output)) + ' teachers found'
    return jsonify({
        'message': message,
        'teachers': output
    }), SUCCESS_CODE



'''
Get a full Teacher object from a Teacher id.

url parameter:
* teacher_id - Teacher id

output:
* message - execution result message
* teacher - serialized Teacher object
'''
@teachers.route('/api/teachers/<teacher_id>', methods = ['GET'])
def get_teacher_by_id(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()

    # Return results
    if not teacher:
        return jsonify({
            'message': f'Teacher account not found'
        }), ERROR_CODE

    output = teacher.serialize()
    return jsonify({
        'message': 'success',
        'teacher': output
    }), SUCCESS_CODE



'''
Update a Teacher account information.

url parameter:
* teacher_id - Teacher id

available request parameters:
* email
* username
* fname
* lname
* display_name

output:
* message - execution result message
* teacher - serialized updated Teacher object
'''
@teachers.route('/api/teachers/<teacher_id>', methods = ['PUT'])
def update_teacher_account(teacher_id):
    # Request checks
    update_info = request.json
    teacher = Teacher.query.filter_by(id = teacher_id).first()

    # Request checks
    if not teacher:
        return jsonify({
            'message': 'Teacher account not found'
        }), ERROR_CODE

    if not update_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE


    # Value assignments
    username = update_info.get('username', teacher.username)
    fname = update_info.get('fname', teacher.fname)
    lname = update_info.get('lname', teacher.lname)
    email = update_info.get('email', teacher.email)
    display_name = update_info.get('display_name', teacher.display_name)

    teacher.username = username
    teacher.fname = fname
    teacher.lname = lname
    teacher.email = email
    teacher.display_name = display_name
    

    # Commit to database
    try:
        db.session.add(teacher)
        db.session.commit()
        output = teacher.serialize()
        return jsonify({
            'message': 'Account updated',
            'teacher': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update account'
        }), ERROR_CODE



'''
Update a Teacher's password'

url parameter:
* teacher_id - Teacher id

required request parameters:
* new_password
* old_password

output:
* message - execution result message
'''
@teachers.route('/auth/teachers/<teacher_id>', methods = ['PUT'])
def update_teacher_password(teacher_id):
    # Request checks
    update_info = request.json
    teacher = Teacher.query.filter_by(id = teacher_id).first()

    # Request checks
    if not teacher:
        return jsonify({
            'message': 'Teacher account not found'
        }), ERROR_CODE

    if not update_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE


    # Value checks
    new_password = update_info.get('new_password', None)
    old_password = update_info.get('old_password', None)

    if not new_password or not old_password:
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE


    # Encode password
    if bcrypt.check_password_hash(teacher.password, old_password.encode('utf-8')):
        encoded_password = new_password.encode('utf-8')
        teacher.password = bcrypt.generate_password_hash(encoded_password).decode('utf-8')
    else:
        return jsonify({
            'message': 'Incorrect password'
        }), ERROR_CODE


    # Commit to database
    try:
        db.session.add(teacher)
        db.session.commit()
        return jsonify({
            'message': 'Password updated'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update password'
        }), ERROR_CODE



'''
Create a Teacher account

url parameter:
* school_id - Teather's School abbreviation

required request parameters:
* email
* username
* display_name
* password
* code

optional request parameters:
* fname
* lname

output:
* message - execution result message
* teacher - serialized newly created Teacher account
'''
@teachers.route('/auth/register/schools/<school_id>/teachers', methods = ['POST'])
def register_teacher_account(school_id):
    # Request checks
    account_info = request.json
    school = School.query.filter_by(abbreviation = school_id).first()

    # Request checks
    if not account_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE

    if not school:
        return jsonify({
            'message': 'School not found'
        }), ERROR_CODE


    # Value checks
    username = account_info.get('username', None)
    password = account_info.get('password', None)
    email = account_info.get('email', None)
    display_name = account_info.get('display_name', None)
    code = account_info.get('code', None)

    if not (password and username and email and display_name and code):
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE

    # verify teacher belongs to the school
    if code != school.signup_code:
        return jsonify({
            'message': 'Incorrect sign up code'
        }), ERROR_CODE

    # verify valid teacher email, if required by school
    if school.domain:
        if (email.split("@",1)[1]) != school.domain:
            return jsonify({
            'message': 'Incorrect school email domain'
        }), ERROR_CODE

    # check if teacher account already exists
    existing_teacher = Teacher.query.filter_by(username = username).first()
    if existing_teacher:
        return jsonify({
            'message': 'Username already exists'
        }), ERROR_CODE


    # Value setting
    fname = account_info.get('fname', None)
    lname = account_info.get('lname', None)
    id = str(uuid.uuid4())
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.generate_password_hash(encoded_password).decode('utf-8') 

    teacher = Teacher(
        id = id,
        username = username,
        password = hashed_password,
        email = email,
        display_name = display_name,
        school = school_id
    )

    if fname:
        teacher.fname = fname
    if lname:
        teacher.lname = lname


    # Commit to database
    try:
        db.session.add(teacher)
        db.session.commit()
        output = teacher.serialize()
        return jsonify({
            'message': 'Account created',
            'teacher': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create account'
        }), ERROR_CODE



'''
Login as a Teacher

url parameter:
* school_id - Teacher's School abbreviation

required request parameters:
* username OR email
* password

output:
* message - execution result message
* teacher - serialized logged in Teacher account
'''
@teachers.route('/auth/schools/<school_id>/teachers/login', methods = ['POST'])
def teacher_login(school_id):
    # Request checks
    credentials = request.json

    # Request checks
    if not credentials:
        return jsonify({
            'message': 'No login credentials provided'
        }), ERROR_CODE

    username = credentials.get('username', None)
    email = credentials.get('email', None)
    password = credentials.get('password', None)

    if not password:
        return jsonify({
            'message': 'Missing password'
        }), ERROR_CODE


    # Value checks
    if username:
        teacher = Teacher.query.filter(db.Teacher.username == username, db.Teacher.school == school_id).first()
    elif email:
        teacher = Teacher.query.filter(db.Teacher.email == email, db.Teacher.school == school_id).first()
    else:
        return jsonify({
            'message': 'Missing username/email'
        }), ERROR_CODE

    if not teacher:
        return jsonify({
            'message': 'Invalid credentials'
        }), ERROR_CODE


    # Attempt login
    encoded_password = password.encode('utf-8')
    if bcrypt.check_password_hash(teacher.password, encoded_password):
        token = 'token'
        output = teacher.serialize()
        return jsonify({
            'message': 'Logged in succesful',
            'token': str(uuid.uuid1()),
            'teacher': output
        }), SUCCESS_CODE

    return jsonify({
            'status': 'fail',
            'message': 'Invalid credentials'
        }), ERROR_CODE



'''
Delete a Teacher account

url parameter:
* teacher_id - Teacher's id

output:
* message - execution result message
'''
@teachers.route('/api/teachers/<teacher_id>', methods = ['DELETE'])
def delete_teacher_account(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()

    # Commit to datbase
    try:
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return jsonify({
                'message': f'Account id: `{teacher_id}` has been deleted'
            }), SUCCESS_CODE
        else:
            return jsonify({
                'message': f'Account id: {teacher_id} does not exist'
            }), ERROR_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete account'
        }), ERROR_CODE

