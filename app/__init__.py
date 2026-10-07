# app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
    app.config['ARTICLES_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'articles')
    
    # Ensure articles directory exists
    os.makedirs(app.config['ARTICLES_DIR'], exist_ok=True)

    # Register Routes (Blueprints)
    from .routes import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
