from flask import Blueprint, request, jsonify

from fopd import db
from fopd.models import Teacher, Device

import uuid, datetime

devices = Blueprint('devices', __name__)

ERROR_CODE = 400
SUCCESS_CODE = 200


'''
Get a list of all Devices that a Teacher has access to.

url parameter:
* teacher_id - Teacher id

output:
* message - execution result message
* devices - list of serialized Device entities
'''
@devices.route('/api/teachers/<teacher_id>/devices', methods = ['GET'])
def get_all_teacher_devices(teacher_id):
    # Request checks
    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Invalid account'
        }), ERROR_CODE

    # Format output
    output = teacher.serialized_devices()
    message = str(len(output)) + ' devices found'

    # Return results
    return jsonify({
        'message': message,
        'devices': output
    }), SUCCESS_CODE


'''
Get a single device's information.

url parameter:
* device_id - Device id

output:
* message - execution result message
* device - serialized Device object
'''
@devices.route('/api/devices/<device_id>', methods = ['GET'])
def get_specific_teacher_device(teacher_id, device_id):
    # Request checks
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({
            'message': 'Invalid device'
        }), ERROR_CODE  

    # Return results
    output = device.serialize()
    return jsonify({
        'message': 'success',
        'device': output
    }), SUCCESS_CODE     


'''
Create a Device

required request parameters:
* id - official FOPD device id
* display_name - name of the Device that shows up on the portal

optional request parameters:
* name - Official Device name

output:
* message - execution result message
* device - serialized newly created Device
'''
@devices.route('/api/devices', methods = ['POST'])
def register_device():
    # Requests check
    device_info = request.json
    if not device_info:
        return jsonify({
            'message': 'No information provided'
        }), ERROR_CODE

    # Value assignment and checks
    device_id = device_info.get('id', None)
    if not teacher_id:
        return jsonify({
            'message': 'Cannot register device without id'
        }), ERROR_CODE

    display = device_info.get('display_name', None)
    if not display:
        return jsonify({
            'message': 'No display name provided'
        }), ERROR_CODE

    # Create Device
    device = Device(
        name = device_info.get('name', None),
        display_name = display,
        id = device_id
    )

    # Commit to db
    try:
        db.session.add(device)
        db.session.commit()
        output = device.serialize()
        return jsonify({
            'message': 'Device created',
            'device': output
            }
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to create device'
        }), ERROR_CODE


'''
Update a device

url parameter:
* device_id - Device id

optional request parameters:
* display_name - name of the Device that shows up on the portal
* name - official Device name
* school - School to assign the deive to

output:
* message - execution result message
* device - serialized newly created Device
'''
@devices.route('/api/devices/<device_id>', methods = ['PUT'])
def update_device(device_id, teacher_id):
    # Request checks
    device_info = request.json
    if not device_info:
        return jsonify({
            'message': 'No information provided'
        }), ERROR_CODE

    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({
            'message': 'Device does not exist'
        }), ERROR_CODE  

    # Value assignment and checks
    device.name = device_info.get('name', device.name) # Should be limited to admin
    deivce.school = device_info.get('school', device.school) # Should be limited to admin
    device.display_name = device_info.get('name', device.display_name)

    # Commit to db
    try:
        db.session.add(device)
        db.session.commit()
        output = device.serialize()
        return jsonify({
            'message': 'Successfully updated',
            'device': output
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unable to update device'
        }), ERROR_CODE

        
'''
Delete a Device from the database (admin)

url parameter:
* device_id - Device's id

output:
* message - execution result message
'''
@devices.route('/api/devices/<device_id>', methods = ['DELETE'])
def delete_device(device_id):
    # Request checks
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({
            'message': 'Device with id {device_id} does not exist'
        }), ERROR_CODE  

    # Commit to db
    try:
        db.session.delete(device)
        db.session.commit()
        return jsonify({
            'message': f'Device id `{device_id}` has been deleted'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': f'Unable to delete device id `{device_id}`'
        }), ERROR_CODE


'''
Remove a Teacher's permissions for a device

url parameter:
* device_id - School abbreviation
* teacher_id - id of the Teacher to remove

output:
* message - execution result message
'''
@devices.route('/api/devices/<device_id>/teachers/<teacher_id>', methods = ['DELETE'])
def remove_teacher_ownership(device_id):
    # Request checks
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({
            'message': f'Device with id {device_id} does not exist'
        }), ERROR_CODE  

    teacher = Teacher.query.filter_by(id = teacher_id).first()
    if not teacher:
        return jsonify({
            'message': 'Teacher account not found'
        }), ERROR_CODE

    # Check Teacher has access to device 
    change_made = False
    removed_relationship = None
    for relationship in db.teacher_devices:
        if relationship.teacher_id == teacher.id and relationship.device_id == device_id:
            removed_relationship = relationship
            change_made == True
            break

    if not change_made:
        return jsonify({
            'message': 'Teacher does not have access to this device'
        }), ERROR_CODE

    # Commit to db
    try:
        db.teacher_devices.remove(removed_relationship)
        db.session.commit()
        return jsonify({
            'message': f'Revoked teacher rights to device  `{device.display_name}`'
        }), SUCCESS_CODE
    except Exception as e:
        print(e)
        return jsonify({
            'message': f'Unable to make change'
        }), ERROR_CODE