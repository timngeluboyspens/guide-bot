# app/__init__.py
from base64 import b64encode
from app.extensions import db, migrate, swagger
from flask import Flask, Response, request, session
from flask_session import Session
from datetime import timedelta
from flask_cors import CORS

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

    from app.routes import api_bp, document_bp, conversations_bp
    CORS(api_bp)
    CORS(document_bp)
    CORS(conversations_bp)
    app.register_blueprint(api_bp)    
    app.register_blueprint(document_bp)
    app.register_blueprint(conversations_bp)

    @app.before_request
    def extend_session_timeout():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
    
    @app.before_request
    def basic_authentication():
        if request.method.lower() == 'options':
            return Response()

    CORS(
        app, 
        origins=["*", "http://localhost:3000"], 
        allow_headers=["Accept", "Content-Type", "Authorization"],
        supports_credentials=True,
        expose_headers=["Accept", "Content-Type", "Authorization"]        
    )
    

    @app.route('/')
    def home():
        return "Welcome to the Guide Bot API!"

    return app
