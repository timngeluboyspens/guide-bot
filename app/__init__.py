# app/__init__.py
from base64 import b64encode
from app.extensions import db, migrate, swagger
from flask import Flask, session
from flask_session import Session
from datetime import timedelta

def create_app():
    
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inisialisasi session
    Session(app)

    # Inisialisasi Swagger
    swagger.init_app(app)
    
    # Define the b64encode filter
    def base64_encode(data):
        return b64encode(data).decode('utf-8')

    # Add the filter to the Jinja2 environment
    app.jinja_env.filters['b64encode'] = base64_encode

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    @app.before_request
    def extend_session_timeout():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)

    @app.route('/')
    def home():
        return "Welcome to the Guide Bot API!"

    return app