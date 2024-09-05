# app/__init__.py
import threading
from flask import Flask, current_app
from base64 import b64encode
from app.extensions import db, migrate
from guide_bot.routes import guide_bot
from app.models import User

def create_app():
    
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Define the b64encode filter
    def base64_encode(data):
        return b64encode(data).decode('utf-8')

    # Add the filter to the Jinja2 environment
    app.jinja_env.filters['b64encode'] = base64_encode

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(guide_bot)

    return app