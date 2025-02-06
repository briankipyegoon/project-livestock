from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.config import create_app, db
from models.models import User,broker
from schemas.schemas import (
    brokers_schema, brokers_schema
)

broker_routes = Blueprint('broker_routes', __name__)
# broker routes
@broker_routes.route('/brokers', methods=['GET'])
@jwt_required()
def get_brokers():
    try:
        brokers = broker.query.all()
        return brokers_schema.jsonify(brokers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@broker_routes.route('/broker/<int:broker_id>', methods=['GET'])
@jwt_required()
def get_broker(broker_id):
    try:
        broker = broker.query.get(broker_id)
        if broker is None:
            return jsonify({"error": "broker not found"}), 404
        return brokers_schema.jsonify(broker), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@broker_routes.route('/broker', methods=['POST'])
@jwt_required()
def add_broker():
    try:
        current_user = get_jwt_identity()
        user_id = request.json['user_id']
        
        if current_user != user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        company_name = request.json['company_name']
        address = request.json.get('address', None)

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_broker = broker(user_id=user_id, company_name=company_name, address=address)
        db.session.add(new_broker)
        db.session.commit()

        return brokers_schema.jsonify(new_broker), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500