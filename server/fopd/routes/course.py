from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Course

import uuid

courses = Blueprint('courses', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Classes belonging to a Teacher.

url parameter:
* teacher_id - Teacher's ID

output:
* message - execution result message
* classes - list of serialized Student accounts
'''
@courses.route('/api/teachers/<teacher_id>/courses', methods = ['GET'])
def get_teacher_courses(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Invalid account'
        }), ERROR_CODE

    output = [i.serialize() for i in teacher.courses]
    
    # Return results
    message = str(len(output)) + ' courses found'
    return jsonify({
        'message': message,
        'courses': output
    })


'''
Get a Class' information.

url parameter:
* teacher_id - Teacher's id who made the class
* course_id - id of Class being accessed

output:
* message - execution result message
* class - serialized Class entity
'''
@courses.route('/api/teachers/<teacher_id>/courses/<course_id>', methods = ['GET'])
def  get_teacher_course_by_id(course_id, teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Invalid account'
        }), ERROR_CODE

    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return jsonify({
            'message': 'Course does not exist'
        }), ERROR_CODE      

    # Temportary auth check
    if course.teacher_id != teacher:
        return jsonify({
            'message': 'Teacher does not have permission to access this course'
        }), ERROR_CODE

    # Return results
    output = course.serialize()
    return jsonify({
        'message': 'success',
        'course': output
    }), SUCCESS_CODE


'''
Delete a Class

url parameter:
* teacher_id - Teacher's id who made the class
* course_id - id of Class being deleted

output:
* message - execution result message
'''
@courses.route('/api/teachers/<teacher_id>/courses/<course_id>', methods = ['DELETE'])
def delete_course_by_teacher(course_id, teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Invalid account'
        }), ERROR_CODE

    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return jsonify({
            'message': 'Course does not exist'
        }), ERROR_CODE      

    # Temportary auth check
    if course.teacher_id != teacher:
        return jsonify({
            'message': 'Teacher does not have permission to access this course'
        }), ERROR_CODE

    # Commit to db
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({
            'message': 'Course deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': f'Cannot delete Course with id: `{course_id}`'
        }), ERROR_CODE


'''
Create a Class

url parameter:
* teacher_id - Teacher's id who is making the class

required request parameters:
* name - name of the new Class

output:
* message - execution result message
* teacher - serialized newly created Teacher account
'''
@courses.route('/api/teachers/<teacher_id>/courses', methods = ['POST'])
def register_course():
    # Request checks
    course_info = request.json

    if not course_info:
        return jsonify({
            'message': 'No course information provided'
        }), ERROR_CODE

    course_name = course_info['name']

    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE


    course = Course(
        name = course_name,
        public_id = str(uuid.uuid4()),
        teacher_id = teacher_id
    )    

    # Commit to db
    try:
        db.session.add(course)
        db.session.commit()
        output = course.serialize()
        return jsonify({
            'message': 'Class created',
            'course': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Class cannot be created'
        }), ERROR_CODE


'''
Update a Class' information.

url parameter:
* teacher_id - Teacher's id who made the class
* course_id - id of Class being updated

available request parameters:
* name - full School name.
* student_ids - a list of ids for the students in the class

output:
* message - execution result message
* class - serialized updated Class entity
'''
@courses.route('/api/teachers/<teacher_id>/courses/<course_id>', methods = ['PUT'])
def update_course(course_id, teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Account does not exist'
        }), ERROR_CODE

    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return jsonify({
            'message': 'Course does not exist'
        }), ERROR_CODE      

    # Temportary auth check
    if course.teacher_id != teacher:
        return jsonify({
            'status': 'fail',
            'message': 'Teacher does not have permission to access this course'
        }), ERROR_CODE

    #Value checks
    course_info = request.json
    if not course_info:
        return jsonify({
            'status': 'fail',
            'message': f'No course information provided to update course `{course_id}`'
        }), ERROR_CODE

    # Set values
    course.name = course_info.get('name', course.name)

    student_ids = course_info.get('student_ids', [])
    course.students = []
    for student_id in student_ids:
        student = Student.query.filter_by(id = student_id).first()
        if student:
            course.students.append(student)

    # Commit to db
    try:
        db.session.add(course)
        db.session.commit()
        output = course.serialize()
        return jsonify({
            'message': 'Course updated',
            'course': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update course information'
        }), ERROR_CODE
