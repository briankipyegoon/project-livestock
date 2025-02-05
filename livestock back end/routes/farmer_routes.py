from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User, Livestock
from schemas.schemas import livestock_schema, livestocks_schema

farmer_routes = Blueprint('farmer_routes', __name__)

@farmer_routes.route('/farmers', methods=['GET'])
def get_farmers():
    try:
        farmers = User.query.filter_by(is_deleted=False).all()
        return jsonify([{
            'id': farmer.id,
            'name': farmer.name,
            'location': farmer.location,
            'phone': farmer.phone,
            'livestock_count': len(farmer.livestock)
        } for farmer in farmers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farmer_routes.route('/farmers/<int:farmer_id>/livestock', methods=['GET'])
def get_farmer_livestock(farmer_id):
    try:
        livestock = Livestock.query.filter_by(
            owner_id=farmer_id,
            is_deleted=False
        ).all()
        return livestocks_schema.jsonify(livestock), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
