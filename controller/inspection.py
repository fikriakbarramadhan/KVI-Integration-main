from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.inspection import Inspection
from datetime import datetime
import uuid

def get_inspection_by_regno():
    # Ensure the user is authorized with a valid JWT token
    try:
        # The @jwt_required decorator will automatically check for the token in the request
        # If the token is missing or invalid, it will raise an error and return 401 Unauthorized
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({
            "code": "ERR992",
            "message": "Forbidden Access",
            "status": 422,
            "path": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 422
    except Exception as e:
        # Handle the error and return custom error response if token is invalid
        return jsonify({
            "code": "ERR992",
            "message": "Forbidden Access",
            "status": 422,
            "path": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 422

    # Get the regNo from the URL parameter
    reg_no = request.view_args.get('regNo')
    
    # Attempt to find the inspection record with the given regNo
    inspection = Inspection.query.filter_by(reg_no=reg_no).first()
    
    # If the record exists
    if inspection:
        return jsonify({
            "status": 1,
            "inspection_id": inspection.inspection_id,
            "trx_id": inspection.trx_id,
            "reg_no": inspection.reg_no,
            "remark_reg_no": inspection.remark_reg_no,
            "engine_no": inspection.engine_no,
            "remark_engine_no": inspection.remark_engine_no,
            "chassis_no": inspection.chassis_no,
            "remark_chassis_no": inspection.remark_chassis_no,
            "front_fid": inspection.front_fid,
            "back_fid": inspection.back_fid,
            "engine_no_fid": inspection.engine_no_fid,
            "chassis_no_fid": inspection.chassis_no_fid,
            "officer": inspection.officer,
            "timestamp": inspection.timestamp
        }), 200
    
    # If no inspection is found for the given regNo
    else:
        return jsonify({
            "status": 99,
            "error_message": "No Data"
        }), 404


def get_image_inspection_by_regno():
    # Ensure the user is authorized with a valid JWT token
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({
            "code": "ERR992",
            "message": "Forbidden Access",
            "status": 422,
            "path": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 422
    except Exception as e:
        return jsonify({
            "code": "ERR992",
            "message": "Forbidden Access",
            "status": 401,
            "path": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 422

    # Get the regNo from the URL parameter
    reg_no = request.view_args.get('regNo')
    
    # Attempt to find the inspection record with the given regNo
    inspection = Inspection.query.filter_by(reg_no=reg_no).first()
    
    # If the record exists
    if inspection:
        return jsonify({
            "status": 1,
            "inspection_id": inspection.inspection_id,
            "trx_id": inspection.trx_id,
            "front": inspection.front_image_base64,  # Base64 image data for front
            "back": inspection.back_image_base64,    # Base64 image data for back
            "engine_no": inspection.engine_no_image_base64,  # Base64 image data for engine no
            "chassis_no": inspection.chassis_no_image_base64,  # Base64 image data for chassis no
            "reg_no": inspection.reg_no_image_base64,  # Base64 image data for registration no
        }), 200
    
    # If no inspection is found for the given regNo
    else:
        return jsonify({
            "status": 99,
            "error_message": "No Data"
        }), 404
