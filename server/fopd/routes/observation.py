from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Student, Teacher, Experiment, Observation, ObservationResponse

import uuid, datetime

observations = Blueprint('observations', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Observations for an Experiment.

url parameter:
* experiment_id - Experiment id

output:
* message - execution result message
* observation - list of serialized Observation entities
'''
@observations.route('/api/experiments/<experiment_id>/observations', methods = ['GET'])
def get_all_observations_by_experiment(experiment_id):
    # Request checks
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE

    # Format output
    output = [i.serialize() for i in student.observations]
    message = str(len(output)) + ' observations found'

    return jsonify({
        'message': message,
        'observations': output
    }), SUCCESS_CODE



'''
Get an Observation's info by id.

url parameter:
* observation_id - observation id

output:
* message - execution result message
* observation - serialized Observation object
'''
@observations.route('/api/observation/<observation_id>', methods = ['GET'])
def get_observation_by_id(observation_id):
    # Request checks
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    # Format output
    output = observation.serialize()

    return jsonify({
        'message': 'success',
        'observation': output
    }), SUCCESS_CODE



'''
Create an Observation

url parameter:
* experiment_id - Experiment id

required request parameters:
* title - Title of the Observation

optional request parameters:
* description - Description of the Observation
* student_ids - List of student IDs for students to assign

output:
* message - execution result message
* observation - serialized newly created Observation
'''
@observations.route('/api/experiments/<experiment_id>/observations', methods = ['POST'])
def create_observation(experiment_id):
    # Request checks
    observation_info = request.json
    if not observation_info:
        return jsonify({
            'message': 'No observation information provided'
        }), ERROR_CODE

    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE


    # Value checks and assignments
    try:
        observation = Observation(
            title = observation_info['title'],
            description = observation_info.get('description', ''),
            updated = datetime.date.today(),
            id = str(uuid.uuid4()),
            experiment_id = experiment_id        
        )
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE

    student_ids = observation_info.get('student_ids', [])
    for student_id in student_ids:
        student = Student.query.filter_by(id = student_id).first()

        if student:
            observation.collaborators.append(student)


    # Commit to db
    try:
        db.session.add(observation)
        db.session.commit()
        output = observation.serialize()
        return jsonify({
            'message': 'Observation created',
            'observation': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create observation'
        }), ERROR_CODE



'''
Update an Observation

url parameter:
* experiment_id - Experiment id
* observation_id - Observation id

optional request parameters:
* title - Title of the Observation
* description - Description of the Observation
* student_ids - New list of assigned students

output:
* message - execution result message
* observation - serialized newly updated Observation
'''
@observations.route('/api/experiments/<experiment_id>/observations/<observation_id>', methods = ['PUT'])
def update_observation(experiment_id, observation_id):
    # Request checks
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    observation_info = request.json
    if not observation_info:
        return jsonify({
            'message': 'No observation information provided'
        }), ERROR_CODE


    # Value assignment and checks
    observation.title = observation_info.get('title', observation.title)
    observation.description = observation_info.get('description', observation.description)
    observation.updated = datetime.date.today()
    
    student_ids = observation_info.get('student_ids', None)
    if student_ids:
        observation.collaborators = []
        for student_id in student_ids:
            student = Student.query.filter_by(id = student_id)
            if student:
                observation.collaborators.append(student)


    # Commit to db
    try:
        db.session.add(observation)
        db.session.commit()
        output = observation.serialize()
        return jsonify({
            'message': 'Observation has been updated',
            'observation': output
        }), SUCCESS_CODE

    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update observation'
        }), ERROR_CODE



'''
Delete an Observation

url parameter:
* observation_id - Observation id

output:
* message - execution result message
'''
@observations.route('/api/observations/<observation_id>', methods = ['DELETE'])
def delete_observation(observation_id):
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    try:
        db.session.delete(observation)
        db.session.commit()
        return jsonify({
            'message': 'Observation has been deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete observation '
        }), ERROR_CODE
