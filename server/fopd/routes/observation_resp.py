from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Student, Teacher, Experiment, Observation, ObservationResponse

import uuid, datetime

observations = Blueprint('observations', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200



'''
Create an Observation Response row

url parameter:
* experiment_id - Experiment id

required request parameters:


optional request parameters:


output:
* message - execution result message
* observation - serialized newly created Observation
'''
@observations.route('/api/observations/<observation_id>/responses', methods = ['POST'])
def add_observation_response(observation_id):
    # Request checks
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    # TODO: Verify teacher

    numResponses = len(observation.serialized_responses())

    response = ObservationResponse(
        position = numResponses,
        observation_id = observation_id
    )

    response.observation = observation

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
            'message': 'Unable to create observation response'
        }), ERROR_CODE



'''
Update an Observation Response

url parameter:
* response_id - Observation Response id
* observation_id - Observation id

required request parameters:
* recorder - who submitted the update

optional request parameters:
* response - Student's response
* position - The position of the response in order

output:
* message - execution result message
* observation - serialized newly updated Observation
'''
@observations.route('/api/observations/<observation_id>/responses/<response_id>', methods = ['PUT'])
def update_observation_response(observation_id, response_id):
    # Request checks
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    obv_response = ObservationResponse.query.filter_by(id = response_id).first()
    if not obv_response:
        return jsonify({
            'message': 'Observation response does not exist'
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
        responses = observation.responses
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
            'message': 'Unable to update observation response'
        }), ERROR_CODE



'''
Lock or unlock an Observations Response

url parameter:
* response_id - Observation Response id
* observation_id - Observation id

required request parameters:


optional request parameters:


output:
* message - execution result message
* observation - serialized newly updated Observation
'''
@observations.route('/api/observation/<observation_id>/response/<response_id>', methods = ['POST'])
def update_observation_response_lock(observation_id, response_id):
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    response = ObservationResponse.query.filter_by(id = response_id).first()
    if not response:
        return jsonify({
            'message': 'Observation response does not exist'
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
            'message': 'Unable to lock observation response'
        }), ERROR_CODE



'''
Get a list of all Observations Responses.

url parameter:
* observation_id - Observation id

output:
* message - execution result message
* responses - list of serialized Observation Response entities
'''
@observations.route('/api/observations/<observation_id>/responses', methods = ['GET'])
def get_all_observation_responses_for_observation(observation_id):
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    responses = observation.serialized_responses()

    return jsonify({
        'message': 'success',
        'responses': responses
    }), SUCCESS_CODE



'''
Delete an Observation Responses

url parameter:
* observation_id - Observation id

output:
* message - execution result message
* responses - list of serialized Observation Response entities
'''
@observations.route('/api/observations/<observation_id>/responses/<response_id>', methods = ['DELETE'])
def delete_observation_response(observation_id, response_id):
    observation = Observation.query.filter_by(id = observation_id).first()
    if not observation:
        return jsonify({
            'message': 'Observation does not exist'
        }), ERROR_CODE

    response = ObservationResponse.query.filter_by(id = response_id).first()
    if not response:
        return jsonify({
            'message': 'Observation response does not exist'
        }), ERROR_CODE

    try:
        db.session.delete(response)
        db.session.commit()
        output = observation.serialized_responses()
        return jsonify({
            'message': 'Observation response has been deleted',
            'responses': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to delete observation response'
        }), ERROR_CODE
