from .user_routes import user_routes
from .farmer_routes import farmer_routes
from .broker_routes import broker_routes
from config.config import create_app

app = create_app()

__all__ = ["user_routes", "farmer_routes", "broker_routes"]