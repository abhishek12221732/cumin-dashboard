import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from models.db import db
import models
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.project_member import project_member_bp
from routes.item import item_bp
from routes.board_column import column_bp
from routes.user import user_bp
from routes.teams import teams_bp
from routes.notification import notification_bp
from routes.reports import reports_bp
from routes.admin import admin_bp
from flask_cors import CORS
from flask import request
from flask_jwt_extended import JWTManager
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

load_dotenv()

app = None # Placeholder

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Default config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = os.environ.get('JWT_HEADER_NAME', 'Authorization')
    app.config['JWT_HEADER_TYPE'] = os.environ.get('JWT_HEADER_TYPE', 'Bearer')

    # Override with test config if passed
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/*": {"origins": os.environ.get('CORS_ORIGINS', '*')}}, allow_headers="*", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(project_member_bp)
    app.register_blueprint(item_bp, url_prefix='/items')
    app.register_blueprint(column_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    
    @app.route('/')
    def index():
        return 'Cumin Dashboard Backend is running!'
        
    with app.app_context():
        db.create_all()
        
    return app

# Main entry point
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
