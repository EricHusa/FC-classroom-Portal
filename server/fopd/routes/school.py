from flask import Blueprint, request, jsonify

from fopd import db, bcrypt
from fopd.models import School
from sqlalchemy import or_

import uuid

schools = Blueprint('schools', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a School object from a school abbreviation.

url parameter:
* abbrev - School abbreviation

output:
* message - execution result message
* school - serialized School object
'''
@schools.route('/api/schools/<abbrev>', methods = ['GET'])
def get_school(abbrev):
    # Request checks
    school = School.query.filter_by(abbreviation = abbrev).first()

    if not school:
        return jsonify({
            'message': 'School not found'
        }), ERROR_CODE
    
    # Return result
    output = school.serialize()
    return jsonify({
        'message': "success",
        'school': output
    }), SUCCESS_CODE



'''
Create a School organization

required request parameters:
* name - full School name.
* abbreviation - School name abbreviation.
* email - primary contact email.
* signup_code - a code Teacher accounts can use to sign up.

optional request parameters:
* domain - an email domain to restrict teacher emails. everything that comes after the @.
* state - US state abbreviation where school is located
* city - US city where school is located
* address - US address where school is located

output:
* message - execution result message
* school - serialized newly created School object
'''
@schools.route('/auth/register/schools', methods = ['POST'])
def register_school():
    school_info = request.json

    # Request checks
    if not school_info:
        return jsonify({
            'message': 'No account information provided'
        }), ERROR_CODE

    required = ['name', 'abbreviation', 'email', 'signup_code']
    for item in required:
        if not school_info.get(item, None):
            return jsonify({
            'message': f'Missing school {item}'
        }), ERROR_CODE


    # Value assignment and checks
    name = school_info.get('name', None)
    abbreviation = school_info.get('abbreviation', None)
    email = school_info.get('email', None)
    signup_code = school_info.get('signup_code', None)

    domain = school_info.get('domain', None)
    state = school_info.get('state', None)
    city = school_info.get('city', None)
    address = school_info.get('address', None)

    if email.find('@') == -1:
        return jsonify({
            'message': 'Invalid email'
        }), ERROR_CODE

    # check if school already exists
    existing_school = School.query.filter(or_(School.abbreviation == abbreviation,School.abbreviation == abbreviation)).first()
    if existing_school:
        return jsonify({
            'message': 'School already exists'
        }), ERROR_CODE


    # Object creation
    school = School(
        name = name,
        abbreviation = abbreviation,
        email = email,
        signup_code = signup_code
    )

    # optional values
    if domain:
        school.domain = domain
    if state:
        school.state = state
    if city:
        school.city = city
    if address:
        school.address = address


    # commit to database
    try:
        db.session.add(school)
        db.session.commit()
        output = school.serialize_full()
        return jsonify({
            'message': 'School created',
            'school': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create School'
        }), ERROR_CODE
    


'''
Update a School's information.

url parameter:
* abbrev - School abbreviation

available request parameters:
* name - full School name.
* abbreviation - School name abbreviation.
* email - primary contact email.
* signup_code - a code Teacher accounts can use to sign up.
* domain - an email domain to restrict teacher emails. everything that comes after the @.
* state - US state abbreviation where school is located
* city - US city where school is located
* address - US address where school is located

output:
* message - execution result message
* school - serialized updated School object
'''
@schools.route('/api/schools/<abbrev>', methods = ['PUT'])
def update_school(abbrev):
    update_info = request.json
    school = School.query.filter_by(abbreviation = abbrev).first()

    # Request checks
    if not update_info:
        return jsonify({
            'message': 'No update information provided'
        }), ERROR_CODE

    if not school:
        return jsonify({
            'message': 'School not found'
        }), ERROR_CODE


    # Value assignments
    school.name = update_info.get('name', school.name)
    school.abbreviation = update_info.get('abbreviation', school.abbreviation)
    school.email = update_info.get('email', school.email)
    school.signup_code = update_info.get('signup_code', school.signup_code)
    school.domain = update_info.get('domain', school.domain)
    school.state = update_info.get('state', school.state)
    school.city = update_info.get('city', school.city)
    school.address = update_info.get('address', school.address)
    

    # Commit to database
    try:
        db.session.add(school)
        db.session.commit()
        output = school.serialize_full()
        return jsonify({
            'message': 'School updated',
            'school': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update School information'
        }), ERROR_CODE


'''
Delete a School

url parameter:
* abbrev - School abbreviation

output:
* message - execution result message
'''
@schools.route('/api/schools/<abbrev>', methods = ['DELETE'])
def delete_school(abbrev):
    school = School.query.filter_by(abbreviation = abbrev).first()
    try:
        if school:
            db.session.delete(school)
            db.session.commit()
            return jsonify({
                'message': f'School `{abbrev}` has been deleted'
            }), SUCCESS_CODE
        else:
            return jsonify({
                'message': f'School `{abbrev}` does not exist'
            }), ERROR_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete School'
        }), ERROR_CODE
