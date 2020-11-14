from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Student, Teacher, Experiment, Device

import uuid, datetime

experiments = Blueprint('experiments', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Experiments belonging to a Student.

url parameter:
* student_id - Student id

output:
* message - execution result message
* experiments - list of serialized Experiment entities
'''
@experiments.route('/api/students/<student_id>/experiments', methods = ['GET'])
def get_teacher_experiments(student_id):
    # Request checks
    student = Student.query.filter_by(id = student_id).first()
    if not student:
        return jsonify({
            'message': 'Invalid account'
        }), ERROR_CODE

    # Format output
    output = [i.serialize() for i in student.experiments]
    message = str(len(output)) + ' experiments found'

    return jsonify({
        'message': message,
        'experiments': output
    }), SUCCESS_CODE


'''
Get an Experiment's info by id.

url parameter:
* experiment_id - Experiment id

output:
* message - execution result message
* experiment - serialized Experiment object
'''
@experiments.route('/api/experiments/<experiment_id>', methods = ['GET'])
def get_experiment_by_id(experiment_id):
    # Request checks
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE

    # TODO: Check user has access

    output = experiment.serialize()

    return jsonify({
        'status': 'success',
        'experiment': output
    }), SUCCESS_CODE


'''
Create an Experiment

url parameter:
* teacher_id - Teacher id

required request parameters:
* title - Title of the Experiment
* plant - What plant is being grown

optional request parameters:
* description - Description of the Experiment
* device_id - The device which the experiment is taking place on
* start_date - The day the Experiment started
* student_ids - A list of Student ids to add students to experiment

output:
* message - execution result message
* experiment - serialized newly created Experiment
'''
@experiments.route('/api/teachers/<teacher_id>/experiments', methods = ['POST'])
def create_experiment(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()

    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    experiment_info = request.json
    if not experiment_info:
        return jsonify({
            'message': 'No experiment information provided'
        }), ERROR_CODE

    # TODO: Check user has access

    # Value assignment and checks
    exp_title = experiment_info.get('title', None)
    if not exp_title:
        return jsonify({
            'message': 'Missing requirement: title'
        }), ERROR_CODE

    exp_plant = experiment_info.get('plant', None)
    if not exp_plant:
        return jsonify({
            'message': 'Missing requirement: plant'
        }), ERROR_CODE

    experiment = Experiment(
        id = str(uuid.uuid4()),
        title = exp_title,
        plant = exp_plant,
        description = experiment_info.get('description', 'No description'),
        start_date = experiment_info.get('start_date', datetime.date.today())
    )
    experiment.teacher = teacher_id
    experiment.device_id = experiment_info.get('device_id', None)

    student_ids = experiment_info.get('student_ids', [])
    experiment.students = []
    if student_ids:
        for student_id in student_ids:
            student = Student.query.filter_by(id = student_id).first()
            if student:
                student.experiments.append(experiment)

    # Commit to db
    try:
        db.session.add(experiment)
        db.session.commit()
        output = experiment.serialized()
        return jsonify({
            'message': 'Successfully created experiment',
            'experiment': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create experiment',
            'error': str(e)
        }), ERROR_CODE


'''
Update an Experiment

url parameter:
* teacher_id - Teacher id
* experiment_id - Experiment id

optional request parameters:
* title - Title of the Experiment
* plant - What plant is being grown
* description - Description of the Experiment
* device_id - The device which the experiment is taking place on
* start_date - The day the Experiment started
* student_ids - A list of Student ids to add students to experiment

output:
* message - execution result message
* experiment - serialized newly updated Experiment
'''
@experiments.route('/api/teachers/<teacher_id>/experiments/<experiment_id>', methods = ['PUT'])
def update_experiment(teacher_id, experiment_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'status': 'fail',
            'message': 'Experiment does not exist'
        }), ERROR_CODE

    experiment_info = request.json
    if not experiment_info:
        return jsonify({
            'message': 'No experiment information provided'
        }), ERROR_CODE

    # Value assignment and checks
    student_ids = experiment_info.get('student_ids', [])
    for student_id in student_ids:
        student = Student.query.filter_by(id = student_id).first()
        if student:
            experiment.students.append(student)

    experiment.title = experiment_info.get('title', experiment.title)
    experiment.plant = experiment_info.get('plant', experiment.plant)
    experiment.description = experiment_info.get('description', experiment.description)
    experiment.device_id = experiment_info.get('device_id', experiment.device_id)
    experiment.start_date = experiment_info.get('start_date', experiment.start_date)


    # Commit to db
    try:
        db.session.add(experiment)
        db.session.commit()
        output = experiment.serialized()
        return jsonify({
            'message': 'Experiment has been updated',
            'experiment': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update course information'
        }), ERROR_CODE


'''
Delete an Experiment

url parameter:
* experiment_id - Experiment id

output:
* message - execution result message
'''
@experiments.route('/api/experiments/<experiment_id>', methods = ['DELETE'])
def delete_experiment(experiment_id):
    # Request checks
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    if not experiment:
        return jsonify({
            'message': 'Experiment does not exist'
        }), ERROR_CODE

    # TODO: Check user owns experiment

    # Commit to db
    try:
        db.session.delete(experiment)
        db.session.commit()
        return jsonify({
            'message': 'Experiment has been deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete experiment'
        }), ERROR_CODE