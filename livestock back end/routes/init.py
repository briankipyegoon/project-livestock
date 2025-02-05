from flask import Blueprint
from routes.livestock_routes import livestock_routes
from routes.farmer_routes import farmer_routes
from routes.broker_routes import broker_routes
from routes.auth_routes import auth_routes

# Initialize blueprints
def init_routes(app):
    # Register blueprints with their URL prefixes
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(livestock_routes, url_prefix='/api')
    app.register_blueprint(farmer_routes, url_prefix='/api')
    app.register_blueprint(broker_routes, url_prefix='/api')

    return app
