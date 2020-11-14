from flask import Blueprint, request, jsonify

from fopd import db, bcrypt
from fopd.models import Student, Teacher, Assignment

import uuid, datetime

assignments = Blueprint('assignments', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Assignments assigned to a Student.

url parameter:
* student_id - Student id

output:
* message - execution result message
* assignments - list of serialized Assignment entities
'''
@assignments.route('/api/students/<student_id>/assignments', methods = ['GET'])
def get_all_student_assignments(student_id):
    # Request checks
    student = Student.query.filter_by(id = student_id).first()
    if not student:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    
    # Format output
    output = [i.serialize() for i in student.assignments]
    message = str(len(output)) + ' assignments found'

    return jsonify({
        'message': message,
        'assignments': output
    }), SUCCESS_CODE



'''
Get a list of all Assignments assigned to a Teacher.

url parameter:
* teacher_id - Teacher id

output:
* message - execution result message
* assignments - list of serialized Assignment entities
'''
@assignments.route('/api/teachers/<teacher_id>/assignments', methods = ['GET'])
def get_all_teacher_assignments(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    # Format output
    output = [i.serialize() for i in teacher.assignments]
    message = str(len(output)) + ' assignments found'

    return jsonify({
        'message': message,
        'assignments': output
    }), SUCCESS_CODE



'''
Get an Assignment's info by id.

url parameter:
* assignment_id - Assignment id

output:
* message - execution result message
* assignment - serialized Assignment object
'''
@assignments.route('/api/assignments/<assignment_id>', methods = ['GET'])
def get_assignment_by_id(assignment_id):
    # Request checks
    assignment = Assignment.query.filter_by(id = assignment_id).first()
    if not assignment:
        return jsonify({
            'message': 'Assignmnet does not exist'
        }), ERROR_CODE

    # TODO: Check user has access

    output = assignment.serialize()

    return jsonify({
        'status': 'success',
        'assignment': output
    }), SUCCESS_CODE



'''
Create an Assignment

url parameter:
* teacher_id - Teacher id

required request parameters:
* title - Title of the Assignment
* category - Which type of assignment (numerical, written)
* due_date - When the assignment is due

optional request parameters:
* description - Description of the Experiment
* units - For numerical assignments, the response units
* student_ids - List of student IDs for students to assign

output:
* message - execution result message
* assignment - serialized newly created Assignment
'''
@assignments.route('/api/teachers/<teacher_id>/assignments', methods = ['POST'])
def create_assignment(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    assignment_info = request.json
    if not assignment_info:
        return jsonify({
            'message': 'No assignment information provided'
        }), ERROR_CODE

    # Value checks and assignments
    try:
        assignment = Assignment(
            title = assignment_info['title'],
            description = assignment_info.get('description', None),
            category = assignment_info['category'],
            due_date = str(assignment_info['due_date']),
            units = assignment_info.get('units', None),
            teacher_id = teacher_id,
            id = str(uuid.uuid4())
        )  
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE

    if(assignment_info['category'] not in ["numerical", "written"]):
        return jsonify({
            'message': 'Assignment category must be either "numerical" or "written"'
        }), ERROR_CODE

    student_ids = assignment_info.get('student_ids', [])
    for student_id in student_ids:
        student = Student.query.filter_by(id = student_id).first()

        if student:
            assignment.students.append(student)


    # Commit to db
    try:
        db.session.add(assignment)
        db.session.commit()
        output = assignment.serialize()
        return jsonify({
            'message': 'Assignment created',
            'assignment': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Assignment not created'
        }), ERROR_CODE



'''
Update an Assignment

url parameter:
* teacher_id - Teacher id
* assignment_id - 

optional request parameters:
* title - Title of the Assignment
* category - What type of Assignment
* description - Description of the Assignment
* due_date - The day the Assignment is due
* units - For numerical assignments, the response units
* student_ids - New list of assigned students

output:
* message - execution result message
* assignment - serialized newly updated Assignment
'''
@assignments.route('/api/teachers/<teacher_id>/assignments/<assignment_id>', methods = ['PUT'])
def update_assignment(teacher_id, assignment_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    assignment = Assignment.query.filter_by(id = assignment_id).first()
    if not assignment:
        return jsonify({
            'message': 'Assignment does not exist'
        }), ERROR_CODE

    if assignment.teacher_id != teacher_id:
        return jsonify({
            'message': 'Teacher not authorized to update assignment'
        }), ERROR_CODE

    assignment_info = request.json
    if not assignment_info:
        return jsonify({
            'message': 'No assignment information provided to update assignment'
        }), ERROR_CODE


    # Value assignment and checks
    assignment.title = assignment_info.get('title', assignment.title)
    assignment.category = assignment_info.get('category', assignment.category)
    assignment.description = assignment_info.get('description', assignment.description)
    assignment.due_date = assignment_info.get('due_date', assignment.due_date)
    assignment.units = assignment_info.get('units', assignment.units)

    if(assignment.category not in ["numerical", "written"]):
        return jsonify({
            'message': 'Assignment category must be either "numerical" or "written"'
        }), ERROR_CODE

    student_ids = assignment_info.get('student_ids', None)
    if student_ids:
        for student_id in student_ids:
            student = Student.query.filter_by(id = student_id).first()

            if student:
                assignment.students.append(student)


    # Commit to db
    try:
        db.session.add(assignment)
        db.session.commit()
        output = assignment.serialize()
        return jsonify({
            'message': 'Assignment has been updated',
            'assignment': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Assignment not created'
        }), ERROR_CODE



'''
Delete an Assignment

url parameter:
* assignment_id - Assignment id

output:
* message - execution result message
'''
@assignments.route('/api/assignments/<assignment_id>', methods = ['DELETE'])
def delete_assignment(assignment_id):
    # Request checks
    assignment = Assignment.query.filter_by(id = assignment_id).first()
    if not assignment:
        return jsonify({
            'message': 'Assignment does not exist'
        }), ERROR_CODE

    # TODO: Check user owns experiment

    try:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({
            'message': 'Assignment has been deleted'
        }), SUCCESS_CODE

    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete assignment'
        }), ERROR_CODE
