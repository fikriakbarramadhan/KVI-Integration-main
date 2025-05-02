from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.inspection import Inspection
from models.user import db  # Import db here to interact with the database
from datetime import datetime
import uuid

# Endpoint untuk mendapatkan data inspeksi berdasarkan reg_no
def get_inspection_by_regno():
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
            "status": 422,
            "path": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 422

    reg_no = request.view_args.get('regNo')
    inspection = Inspection.query.filter_by(reg_no=reg_no).first()
    
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
    else:
        return jsonify({
            "status": 99,
            "error_message": "No Data"
        }), 404

# Endpoint untuk mendapatkan gambar inspeksi berdasarkan reg_no
def get_image_inspection_by_regno():
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

    reg_no = request.view_args.get('regNo')
    inspection = Inspection.query.filter_by(reg_no=reg_no).first()
    
    if inspection:
        return jsonify({
            "status": 1,
            "inspection_id": inspection.inspection_id,
            "trx_id": inspection.trx_id,
            "front": inspection.front_image_base64,
            "back": inspection.back_image_base64,
            "engine_no": inspection.engine_no_image_base64,
            "chassis_no": inspection.chassis_no_image_base64,
            "reg_no": inspection.reg_no_image_base64,
        }), 200
    else:
        return jsonify({
            "status": 99,
            "error_message": "No Data"
        }), 404

# Endpoint untuk membuat inspeksi baru
def create_inspection():
    try:
        data = request.get_json()

        required_fields = ["trx_id", "reg_no", "engine_no", "chassis_no", "officer"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": 99, "error_message": f"Missing {field}"}), 400

        new_inspection = Inspection(
            trx_id=data["trx_id"],
            reg_no=data["reg_no"],
            remark_reg_no=data.get("remark_reg_no", ""),
            engine_no=data["engine_no"],
            remark_engine_no=data.get("remark_engine_no", ""),
            chassis_no=data["chassis_no"],
            remark_chassis_no=data.get("remark_chassis_no", ""),
            front_fid=data.get("front_fid", ""),
            back_fid=data.get("back_fid", ""),
            engine_no_fid=data.get("engine_no_fid", ""),
            chassis_no_fid=data.get("chassis_no_fid", ""),
            front_image_base64=data.get("front_image_base64", ""),
            back_image_base64=data.get("back_image_base64", ""),
            engine_no_image_base64=data.get("engine_no_image_base64", ""),
            chassis_no_image_base64=data.get("chassis_no_image_base64", ""),
            reg_no_image_base64=data.get("reg_no_image_base64", ""),
            officer=data["officer"],
            timestamp=datetime.utcnow()
        )

        db.session.add(new_inspection)
        db.session.commit()

        return jsonify({
            "status": 1,
            "message": "Inspection created successfully",
            "inspection_id": new_inspection.inspection_id  # Return the generated ID
        }), 201

    except Exception as e:
        return jsonify({
            "status": 99,
            "error_message": f"Error creating inspection: {str(e)}"
        }), 500

# Endpoint untuk menghapus inspeksi berdasarkan inspection_id
def delete_inspection(inspection_id):
    try:
        # Find inspection by inspection_id
        inspection = Inspection.query.filter_by(inspection_id=inspection_id).first()

        if not inspection:
            return jsonify({
                "status": 99,
                "error_message": "Inspection not found"
            }), 404

        db.session.delete(inspection)
        db.session.commit()

        return jsonify({
            "status": 1,
            "message": "Inspection deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status": 99,
            "error_message": f"Error deleting inspection: {str(e)}"
        }), 500

# Endpoint untuk memperbarui inspeksi berdasarkan inspection_id
def update_inspection(inspection_id):
    try:
        # Find inspection by inspection_id
        inspection = Inspection.query.filter_by(inspection_id=inspection_id).first()

        if not inspection:
            return jsonify({
                "status": 99,
                "error_message": "Inspection not found"
            }), 404

        data = request.get_json()

        inspection.trx_id = data.get("trx_id", inspection.trx_id)
        inspection.remark_reg_no = data.get("remark_reg_no", inspection.remark_reg_no)
        inspection.engine_no = data.get("engine_no", inspection.engine_no)
        inspection.remark_engine_no = data.get("remark_engine_no", inspection.remark_engine_no)
        inspection.chassis_no = data.get("chassis_no", inspection.chassis_no)
        inspection.remark_chassis_no = data.get("remark_chassis_no", inspection.remark_chassis_no)
        inspection.front_fid = data.get("front_fid", inspection.front_fid)
        inspection.back_fid = data.get("back_fid", inspection.back_fid)
        inspection.engine_no_fid = data.get("engine_no_fid", inspection.engine_no_fid)
        inspection.chassis_no_fid = data.get("chassis_no_fid", inspection.chassis_no_fid)
        inspection.front_image_base64 = data.get("front_image_base64", inspection.front_image_base64)
        inspection.back_image_base64 = data.get("back_image_base64", inspection.back_image_base64)
        inspection.engine_no_image_base64 = data.get("engine_no_image_base64", inspection.engine_no_image_base64)
        inspection.chassis_no_image_base64 = data.get("chassis_no_image_base64", inspection.chassis_no_image_base64)
        inspection.reg_no_image_base64 = data.get("reg_no_image_base64", inspection.reg_no_image_base64)
        inspection.officer = data.get("officer", inspection.officer)

        db.session.commit()

        return jsonify({
            "status": 1,
            "message": "Inspection updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status": 99,
            "error_message": f"Error updating inspection: {str(e)}"
        }), 500
