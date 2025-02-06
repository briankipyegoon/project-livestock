from flask import Blueprint, request, jsonify
from models.models import db, livestock  

# Define the Blueprint
livestock_bp = Blueprint("livestock _bp", __name__)


@livestock_bp.route("/livestock ", methods=["GET"])
def get_products():
    livestock  = livestock .query.all()
    return jsonify([livestock .to_dict() for livestock  in livestock ])

@livestock_bp.route("/livestock ", methods=["POST"])
def add_product():
    try:
        data = request.get_json()  # Ensure JSON is received

        # Validate required fields (without livestock _id)
        required_fields = ["livestock", "breed", "age", "image_url", "description", "location", "phone"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Provide a default farmer_id or set to None 
        farmer_id = data.get("farmer_id", None)  # Set None or default value if missing

        new_livestock = livestock(
            livestock=data["livestock"],
            breed=float(data["breed"]),
            image_url=data["image_url"],
            description=data["description"],
            location=data["location"],
            phone=data["phone"],
            farmer_id=farmer_id
        )

        db.session.add(new_livestock)
        db.session.commit()
        return jsonify(new_livestock.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error response