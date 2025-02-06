from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from config.config import create_app,db
from models.models import User, Farmer
from schemas.schemas import ( 
    farmer_schema, farmers_schema, 
)

farmer_routes = Blueprint('farmer_routes', __name__)
# Farmer routes
@farmer_routes.route('/farmers', methods=['GET'])
@jwt_required()
def get_farmers():
    try:
        farmers = Farmer.query.all()
        return farmers_schema.jsonify(farmers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farmer_routes.route('/farmers/<int:farmer_id>', methods=['GET'])
@jwt_required()
def get_farmer(farmer_id):
    try:
        farmer = Farmer.query.get(farmer_id)
        if farmer is None:
            return jsonify({"error": "Farmer not found"}), 404
        return farmer_schema.jsonify(farmer), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farmer_routes.route('/farmers', methods=['POST'])
@jwt_required()
def add_farmer():
    try:
        current_user = get_jwt_identity()
        user_id = request.json['user_id']
        
        if current_user != user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        farm_name = request.json['farm_name']
        farm_location = request.json.get('farm_location', None)

        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_farmer = Farmer(user_id=user_id, farm_name=farm_name, farm_location=farm_location)
        db.session.add(new_farmer)
        db.session.commit()

        return farmer_schema.jsonify(new_farmer), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@farmer_routes.route('/farmers/location/<location>', methods=['GET'])
@jwt_required()
def get_farmers_by_location(location):
    try:
        farmers = Farmer.query.filter(Farmer.farm_location.ilike(f"%{location}%")).all()
        return farmers_schema.jsonify(farmers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
