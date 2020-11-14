from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Student, Teacher, Experiment, Measurement, MeasurementResponse

import uuid, datetime

measurements = Blueprint('measurements', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200



'''
Create an Measurement Response row

url parameter:
* experiment_id - Experiment id

required request parameters:


optional request parameters:


output:
* message - execution result message
* measurement - serialized newly created Measurement
'''
@measurements.route('/api/measurements/<measurement_id>/responses', methods = ['POST'])
def add_measurement_response(measurement_id):
    # Request checks
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    # TODO: Verify teacher

    numResponses = len(measurement.serialized_responses())

    response = MeasurementResponse(
        position = numResponses,
        measurement_id = measurement_id
    )

    response.measurement = measurement

    try:
        db.session.add(response)
        db.session.commit()
        output = response.serialize()
        return jsonify({
            'message': 'Response slot created',
            'response': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create measurement response'
        }), ERROR_CODE



'''
Update an Measurement Response

url parameter:
* response_id - Measurement Response id
* measurement_id - Measurement id

required request parameters:
* recorder - who submitted the update

optional request parameters:
* response - Student's response
* position - The position of the response in order

output:
* message - execution result message
* measurement - serialized newly updated Measurement
'''
@measurements.route('/api/measurements/<measurement_id>/responses/<response_id>', methods = ['PUT'])
def update_measurement_response(measurement_id, response_id):
    # Request checks
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    obv_response = MeasurementResponse.query.filter_by(id = response_id).first()
    if not obv_response:
        return jsonify({
            'message': 'Measurement response does not exist'
        }), ERROR_CODE

    if obv_response.editable == False:
        return jsonify({
            'message': 'Response cannot be edited'
        }), ERROR_CODE

    response_info = request.json
    if not response_info:
        return jsonify({
            'message': 'No response information provided'
        }), ERROR_CODE

    # Value assignment and checks
    recorder = response_info.get('recorder', None)
    if not recorder:
        return jsonify({
            'message': 'Missing required information'
        }), ERROR_CODE

    new_pos = response_info.get('position', None)
    if new_pos != None:
        responses = measurement.responses
        try:
            for i in range(new_pos, len(responses)):
                responses[i].position = 1 + i
            obv_response.position = response_info['position']
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Unable to adjust response positions'
            }), ERROR_CODE


    obv_response.recorded_by = recorder
    obv_response.response = response_info.get('response', obv_response.response)
    obv_response.submitted = datetime.date.today
    obv_response.editable = False
    
    try:
        db.session.add(obv_response)
        db.session.commit()
        output = obv_response.serialize()
        return jsonify({
            'message': 'Response updated',
            'response': output
        }), SUCCESS_CODE

    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update measurement response'
        }), ERROR_CODE



'''
Lock or unlock an Measurements Response

url parameter:
* response_id - Measurement Response id
* measurement_id - Measurement id

required request parameters:


optional request parameters:


output:
* message - execution result message
* measurement - serialized newly updated Measurement
'''
@measurements.route('/api/measurement/<measurement_id>/response/<response_id>', methods = ['POST'])
def update_measurement_response_lock(measurement_id, response_id):
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    response = MeasurementResponse.query.filter_by(id = response_id).first()
    if not response:
        return jsonify({
            'message': 'Measurement response does not exist'
        }), ERROR_CODE

    response.editable = not response.editable
    
    try:
        db.session.add(response)
        db.session.commit()
        output = response.serialize()
        return jsonify({
            'message': 'Response updated',
            'response': output
        }), SUCCESS_CODE

    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to lock measurement response'
        }), ERROR_CODE



'''
Get a list of all Measurements Responses.

url parameter:
* measurement_id - Measurement id

output:
* message - execution result message
* responses - list of serialized Measurement Response entities
'''
@measurements.route('/api/measurements/<measurement_id>/responses', methods = ['GET'])
def get_all_measurement_responses_for_measurement(measurement_id):
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    responses = measurement.serialized_responses()

    return jsonify({
        'message': 'success',
        'responses': responses
    }), SUCCESS_CODE



'''
Delete an Measurement Responses

url parameter:
* measurement_id - Measurement id

output:
* message - execution result message
* responses - list of serialized Measurement Response entities
'''
@measurements.route('/api/measurements/<measurement_id>/responses/<response_id>', methods = ['DELETE'])
def delete_measurement_response(measurement_id, response_id):
    measurement = Measurement.query.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify({
            'message': 'Measurement does not exist'
        }), ERROR_CODE

    response = MeasurementResponse.query.filter_by(id = response_id).first()
    if not response:
        return jsonify({
            'message': 'Measurement response does not exist'
        }), ERROR_CODE

    try:
        db.session.delete(response)
        db.session.commit()
        output = measurement.serialized_responses()
        return jsonify({
            'message': 'Measurement response has been deleted',
            'responses': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete measurement response'
        }), ERROR_CODE
