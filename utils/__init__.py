from dotenv import load_dotenv
load_dotenv()   # 🔴 MUST BE FIRST

from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    templates_path = os.path.join(base_dir, "templates")

    app = Flask(
        __name__,
        template_folder=templates_path,
        static_folder=os.path.join(base_dir, "static")
    )

    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    
    from routes.routes import register_routes
    register_routes(app)

    return app
