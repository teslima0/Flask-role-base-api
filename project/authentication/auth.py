from flask import Flask, jsonify, request,Blueprint,make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash
from ..models import Admin,CustomUser,Staff,Student,UserRole
from ..import db,app
from bcrypt import hashpw, gensalt
import bcrypt
auths= Blueprint("auths",__name__)
# Register endpoints
from flask_jwt_extended import create_access_token, jwt_required

@auths.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = CustomUser.query.filter_by(email=email).first()

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=user)  
        return jsonify({'access_token': access_token}), 200




@auths.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not role or not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check that the role provided is valid
    if role not in [r.value for r in UserRole]:

        return jsonify({'message': 'Invalid role specified'}), 400

    # Check that the email is not already in use
    if CustomUser.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already in use'}), 400

    # Create a new user object with the specified role
    if role == UserRole.ADMIN.value:
        user = Admin(username=username, email=email)
    elif role == UserRole.STAFF.value:
        user = Staff(username=username, email=email)
    else:
        user = Student(username=username, email=email)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user.password_hash = hashed_password.decode('utf-8')

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

    
# Protected endpoints

@auths.route('/protected/admin', methods=['GET'])
@jwt_required()
def protected_admin():
    current_user_id = get_jwt_identity()
    admin = Admin.query.get(current_user_id)
    if not admin:
        return jsonify({'message': 'Admin not found'}), 404
    return jsonify({'message': 'Hello admin!'}), 200

@auths.route('/protected/staff', methods=['GET'])
@jwt_required()
def protected_staff():
    current_user_id = get_jwt_identity()
    staff = Staff.query.get(current_user_id)
    if not staff:
        return jsonify({'message': 'Staff not found'}), 404
    return jsonify({'message': 'Hello staff!'}), 200


