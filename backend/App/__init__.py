from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    mongo.init_app(app)
    CORS(app)
    jwt.init_app(app)

    # Register blueprints
    from App.routes.user_routes import user_bp
    from App.routes.event_routes import event_bp
    from App.routes.admin_routes import admin_bp
    from App.routes.auth_routes import auth_bp
    from App.routes.interest_routes import interest_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(event_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(interest_bp, url_prefix='/api')

    # Create geospatial index for events
    with app.app_context():
        mongo.db.events.create_index([("location.coordinates", "2dsphere")])

    @app.route('/')
    def index():
        return {"message": "Welcome to Community Pulse API"}

    return app
