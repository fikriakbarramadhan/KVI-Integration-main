from flask import Flask, jsonify, request
from models.user import db, User
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta
import uuid

def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"Message": "Username and password are required"}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"Message": "Username already exists"}), 400

    # Create new user instance
    new_user = User(username=username)
    new_user.set_password(password)

    try:
        db.session.add(new_user)  # Add to session
        db.session.commit()  # Commit to the database
        return jsonify({"Message": f"User {username} registered successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"Message": f"Error registering user: {str(e)}"}), 500

def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Check if the request body is missing or empty
    if not username or not password:
        if not username and not password:
            return jsonify({
                "code": "ERR995",
                "message": "Required Request Body is Missing or Empty",
                "status": 400,
                "path": "/auth",
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
                "uuid": str(uuid.uuid4())
            }), 400

    # Check if password is empty but username matches
    if username and not password:
        return jsonify({
            "code": "ERR998",
            "message": "Password must not be nulled",
            "status": 400,
            "path": "/auth",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 400

    # Check if user exists and password is correct
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # Create JWT access token
        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=60))
        return jsonify({
            "access_token": access_token,
            "token_type": "bearer",
            "message": "Authentication successful"
        }), 200
    else:
        return jsonify({
            "code": "ERR991",
            "message": "Invalid username or password",
            "status": 401,
            "path": "/auth",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "uuid": str(uuid.uuid4())
        }), 401

