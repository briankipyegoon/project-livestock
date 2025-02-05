from flask import jsonify, request, Blueprint
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, 
    create_access_token, create_refresh_token
)
from config.config2 import db
from models.models import User
from schemas.schemas import user_schema, users_schema
import bcrypt

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        role = request.json.get('role', 'user')  # Default to 'user' if not specified
        password = request.json['password']

        if not name or not email or not phone or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate email format
        if not User.is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate phone format
        if not User.is_valid_phone(phone):
            return jsonify({"error": "Phone must be 10 digits"}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        # Validate role
        if role not in ['user', 'farmer', 'broker', 'admin']:
            return jsonify({"error": "Invalid role"}), 400

        # Generate salt and hash password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Create new user
        new_user = User(
            name=name, 
            email=email, 
            phone=phone, 
            role=role, 
            password_hash=password_hash.decode('utf-8'),
        )
        
        db.session.add(new_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=new_user.id)
        
        return jsonify({
            "message": "Registration successful",
            "user": user_schema.dump(new_user),
            "access_token": access_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.query.filter_by(email=email, is_deleted=False).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 403

        if not bcrypt.checkpw(password.encode('utf8'), user.password_hash.encode('utf8')):
            return jsonify({"error": "Invalid password"}), 401

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "user": user_schema.dump(user),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id, is_deleted=False).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_routes.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id, is_deleted=False).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update fields if provided
        if 'name' in request.json:
            user.name = request.json['name']
        if 'phone' in request.json:
            if not User.is_valid_phone(request.json['phone']):
                return jsonify({"error": "Phone must be 10 digits"}), 400
            user.phone = request.json['phone']
        if 'password' in request.json:
            if not User.is_valid_password(request.json['password']):
                return jsonify({"error": "Invalid password format"}), 400
            salt = bcrypt.gensalt()
            user.password_hash = bcrypt.hashpw(
                request.json['password'].encode('utf-8'), 
                salt
            ).decode('utf-8')

        db.session.commit()
        return user_schema.jsonify(user), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_routes.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id, is_deleted=False).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.soft_delete()
        db.session.commit()
        
        return jsonify({"message": "Profile deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500 