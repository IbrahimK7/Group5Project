from flask import Flask

def create_app():
    app = Flask(__name__)
    # register routes from the routes module
    from .routes import register_routes
    register_routes(app)
    return app