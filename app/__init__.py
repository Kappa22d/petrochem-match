"""Application factory and initialization."""
import os
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import Config, DevelopmentConfig, ProductionConfig

# Initialize extensions (will be populated later)
login_manager = LoginManager()
Base = declarative_base()

# Global db session (we'll use SQLAlchemy)
db = None

def create_app(environment='development'):
    """Application factory."""
    global db
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if environment == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Initialize database (using Supabase + SQLAlchemy)
    from app.models import init_db
    db = init_db(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_filters(app)
    
    return app

def register_blueprints(app):
    """Register all route blueprints."""
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.profile import profile_bp
    from app.blueprints.directory import directory_bp
    from app.blueprints.matching import matching_bp
    from app.blueprints.rfq import rfq_bp
    from app.blueprints.tools import tools_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(directory_bp, url_prefix='/directory')
    app.register_blueprint(matching_bp, url_prefix='/matching')
    app.register_blueprint(rfq_bp, url_prefix='/rfq')
    app.register_blueprint(tools_bp, url_prefix='/tools')

def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Server error'}, 500

def register_filters(app):
    """Register Jinja2 filters."""
    @app.template_filter('truncate')
    def truncate_text(text, length=100):
        if len(text) > length:
            return text[:length] + '...'
        return text
