from config.config import create_app
from flask import jsonify, request
from flask_jwt_extended import JWTManager

app = create_app()
# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# JWT error handlers
@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized access"}), 401

@app.errorhandler(422)
def unprocessable_entity_error(error):
    return jsonify({"error": "Unprocessable entity"}), 422

# JWT configuration
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": "Token has expired",
        "message": "Please log in again"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "Invalid token",
        "message": "Please provide a valid token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": "Authorization required",
        "message": "Token is missing"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)