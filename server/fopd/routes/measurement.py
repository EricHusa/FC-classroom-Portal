from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Student, Teacher, Experiment, Measurement, MeasurementResponse

import uuid, datetime

measurements = Blueprint('measurements', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Measurements for an Experiment.

url parameter:
* experiment_id - Experiment id

output:
* message - execution result message
* measurement - list of serialized Measurement entities
'''
@measurements.route('/api/experiments/<experiment_id>/measurements', methods = ['GET'])
def get_all_measurements_by_experiment(experiment_id):
    # Request checks
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE

    # Format output
    output = [i.serialize() for i in student.measurements]
    message = str(len(output)) + ' measurements found'

    return jsonify({
        'message': message,
        'measurements': output
    }), SUCCESS_CODE



'''
Get an Measurement's info by id.

url parameter:
* measurement_id - measurement id

output:
* message - execution result message
* measurement - serialized Measurement object
'''
@measurements.route('/api/measurement/<measurement_id>', methods = ['GET'])
def get_measurement_by_id(measurement_id):
    # Request checks
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    # Format output
    output = measurement.serialize()

    return jsonify({
        'message': 'success',
        'measurement': output
    }), SUCCESS_CODE



'''
Create an Measurement

url parameter:
* experiment_id - Experiment id

required request parameters:
* title - Title of the Measurement
* units - What units to label the response with

optional request parameters:
* description - Description of the Measurement
* graphics - Whether to show the Measurement as a graph in the Data tab
* public - Whether the graph in the Data tab is viewable by all students or just those assigned
* student_ids - List of student IDs for students to assign


output:
* message - execution result message
* measurement - serialized newly created Measurement
'''
@measurements.route('/api/experiments/<experiment_id>/measurements', methods = ['POST'])
def create_measurement(experiment_id):
    # Request checks
    measurement_info = request.json
    if not measurement_info:
        return jsonify({
            'message': 'No measurement information provided'
        }), ERROR_CODE

    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE


    # Value checks and assignments
    try:
        measurement = Measurement(
            title = measurement_info['title'],
            description = measurement_info.get('description', ''),
            units = measurement_info['units'],
            graphics = measurement_info.get('graphics', True),
            public = measurement_info.get('public', False),
            updated = datetime.date.today(),
            id = str(uuid.uuid4()),
            experiment_id = experiment_id        
        )
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE

    student_ids = measurement_info.get('student_ids', [])
    for student_id in student_ids:
        student = Student.query.filter_by(id = student_id).first()

        if student:
            measurement.collaborators.append(student)


    # Commit to db
    try:
        db.session.add(measurement)
        db.session.commit()
        output = measurement.serialize()
        return jsonify({
            'message': 'Measurement created',
            'measurement': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create measurement'
        }), ERROR_CODE



'''
Update an Measurement

url parameter:
* experiment_id - Experiment id
* measurement_id - Measurement id

optional request parameters:
* title - Title of the Measurement
* description - Description of the Measurement
* student_ids - New list of assigned students

output:
* message - execution result message
* measurement - serialized newly updated Measurement
'''
@measurements.route('/api/experiments/<experiment_id>/measurements/<measurement_id>', methods = ['PUT'])
def update_measurement(experiment_id, measurement_id):
    # Request checks
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    measurement_info = request.json
    if not measurement_info:
        return jsonify({
            'message': 'No measurement information provided'
        }), ERROR_CODE


    # Value assignment and checks
    measurement.title = measurement_info.get('title', measurement.title)
    measurement.description = measurement_info.get('description', measurement.description)
    measurement.graphics = measurement_info.get('graphics', measurement.graphics)
    measurement.public = measurement_info.get('public', measurement.public)
    measurement.updated = datetime.date.today()
    
    student_ids = measurement_info.get('student_ids', None)
    if student_ids:
        measurement.collaborators = []
        for student_id in student_ids:
            student = Student.query.filter_by(id = student_id)
            if student:
                measurement.collaborators.append(student)


    # Commit to db
    try:
        db.session.add(measurement)
        db.session.commit()
        output = measurement.serialize()
        return jsonify({
            'message': 'Measurement has been updated',
            'measurement': output
        }), SUCCESS_CODE

    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update measurement'
        }), ERROR_CODE



'''
Delete an Measurement

url parameter:
* measurement_id - Measurement id

output:
* message - execution result message
'''
@measurements.route('/api/measurements/<measurement_id>', methods = ['DELETE'])
def delete_measurement(measurement_id):
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    try:
        db.session.delete(measurement)
        db.session.commit()
        return jsonify({
            'message': 'Measurement has been deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete measurement '
        }), ERROR_CODE
