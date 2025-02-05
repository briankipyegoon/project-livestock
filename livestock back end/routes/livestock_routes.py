from flask import jsonify, request, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from config.config2 import db
from models.models import User, Livestock
from schemas.schemas import livestock_schema, livestocks_schema

livestock_routes = Blueprint('livestock_routes', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@livestock_routes.route('/livestock', methods=['GET'])
def get_livestock_list():
    try:
        livestock = Livestock.query.filter_by(is_deleted=False).all()
        return livestocks_schema.jsonify(livestock), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@livestock_routes.route('/livestock/<int:livestock_id>', methods=['GET'])
def get_livestock(livestock_id):
    try:
        livestock = Livestock.query.get(livestock_id)
        if livestock is None or livestock.is_deleted:
            return jsonify({"error": "Livestock not found"}), 404
        return livestock_schema.jsonify(livestock), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@livestock_routes.route('/livestock', methods=['POST'])
@jwt_required()
def add_livestock():
    try:
        current_user_id = get_jwt_identity()
        
        # Handle image upload
        image = request.files.get('image')
        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_path = f'/uploads/livestock/{filename}'

        new_livestock = Livestock(
            breed=request.form['breed'],
            age=request.form['age'],
            weight=request.form['weight'],
            price=float(request.form['price']),
            location=request.form['location'],
            description=request.form.get('description'),
            image=image_path,
            owner_id=current_user_id
        )

        db.session.add(new_livestock)
        db.session.commit()

        return livestock_schema.jsonify(new_livestock), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@livestock_routes.route('/livestock/<int:livestock_id>', methods=['PUT'])
@jwt_required()
def update_livestock(livestock_id):
    try:
        current_user_id = get_jwt_identity()
        livestock = Livestock.query.get(livestock_id)

        if not livestock or livestock.is_deleted:
            return jsonify({"error": "Livestock not found"}), 404

        if livestock.owner_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403

        # Handle image upload if new image is provided
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            livestock.image = f'/uploads/livestock/{filename}'

        # Update other fields
        livestock.breed = request.form.get('breed', livestock.breed)
        livestock.age = request.form.get('age', livestock.age)
        livestock.weight = request.form.get('weight', livestock.weight)
        livestock.price = float(request.form.get('price', livestock.price))
        livestock.location = request.form.get('location', livestock.location)
        livestock.description = request.form.get('description', livestock.description)

        db.session.commit()
        return livestock_schema.jsonify(livestock), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@livestock_routes.route('/livestock/<int:livestock_id>', methods=['DELETE'])
@jwt_required()
def delete_livestock(livestock_id):
    try:
        current_user_id = get_jwt_identity()
        livestock = Livestock.query.get(livestock_id)

        if not livestock or livestock.is_deleted:
            return jsonify({"error": "Livestock not found"}), 404

        if livestock.owner_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403

        livestock.soft_delete()
        db.session.commit()

        return jsonify({"message": "Livestock deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@livestock_routes.route('/my-livestock', methods=['GET'])
@jwt_required()
def get_user_livestock():
    try:
        current_user_id = get_jwt_identity()
        livestock = Livestock.query.filter_by(
            owner_id=current_user_id,
            is_deleted=False
        ).all()
        return livestocks_schema.jsonify(livestock), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
