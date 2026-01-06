from .home import register_home_routes
from .auth import register_auth_routes

def register_routes(app):
    register_home_routes(app)
    register_auth_routes(app)
