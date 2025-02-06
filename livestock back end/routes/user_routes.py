from flask import jsonify, request, Blueprint
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, 
    create_access_token, create_refresh_token
)
from werkzeug.security import generate_password_hash, check_password_hash
from config.config import create_app,db
from models.models import User, Farmer, Supplier
from schemas.schemas import (
    user_schema, users_schema
)
import bcrypt

user_routes = Blueprint('user_routes', __name__)

# User routes
@user_routes.route('/register', methods=['POST'])
def register():
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        role = request.json['role']
        password = request.json['password_hash']

        if not name or not email or not phone or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

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
        db.session.flush()  # This gets us the user.id before committing

        # Based on role, create corresponding record
        if role.lower() == 'farmer':
            farm_name = request.json.get('farm_name')
            farm_location = request.json.get('farm_location')
            
            if not farm_name:
                return jsonify({"error": "Farm name is required for farmers"}), 400
                
            farmer = Farmer(
                user_id=new_user.id,
                farm_name=farm_name,
                farm_location=farm_location
            )
            db.session.add(farmer)
            
        elif role.lower() == 'broker':
            company_name = request.json.get('company_name')
            address = request.json.get('address')
            
            if not company_name:
                return jsonify({"error": "Company name is required for "}), 400
                
            broker = broker(
                user_id=new_user.id,
                company_name=company_name,
                address=address
            )
            db.session.add(broker)

        db.session.commit()
        return user_schema.jsonify(new_user), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.query.filter_by(email=email).first()

        print(user)
        print(user.password_hash)
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(password.encode('utf8'),user.password_hash.encode('utf8')):
            return jsonify({"error": "Invalid password"})

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

@user_routes.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        return users_schema.jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route('/users', methods=['POST'])
def add_user():
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        role = request.json['role']
        password_hash = request.json['password_hash']
        
        if not name or not email or not phone:
            return jsonify({"error": "Missing required fields"}), 400

        new_user = User(name=name, email=email, phone=phone, role=role, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route('/users/role/<role>', methods=['GET'])
@jwt_required()
def get_users_by_role(role):
    try:
        users = User.query.filter_by(role=role).all()
        return users_schema.jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500