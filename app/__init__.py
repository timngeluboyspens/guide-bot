# app/__init__.py
from base64 import b64encode
import os
import signal
import threading
from app.extensions import db, migrate, swagger
from flask import Flask, Response, request, session
from flask_session import Session
from datetime import timedelta
from flask_cors import CORS

from app.telegram_bot import TelegramBot

bot_thread = None
bot = None
import asyncio

def polling_bot():
    global bot

    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_USERNAME = "@bambubot"

    print('Starting bot...')
    bot = TelegramBot(TOKEN, BOT_USERNAME)

    bot.run()
    
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(bot.run())

# def handle_shutdown_signal(signal, frame):
#     global bot_thread
#     global bot

#     if bot is not None:
#         bot.stop()

#     if bot_thread is not None:
#         print('Shutting down bot...')
#         bot_thread.join()
#         bot_thread = None
#         print('Bot has been shut down.')

#     print('Shutting down the server...')
#     os._exit(0)

def create_app():
    global bot_thread
    
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

    bot_thread = threading.Thread(target=polling_bot, name="TelegramBot")
    bot_thread.start()

    # Tangkap sinyal SIGINT (Ctrl+C) dan SIGTERM
    # signal.signal(signal.SIGINT, handle_shutdown_signal)
    # signal.signal(signal.SIGTERM, handle_shutdown_signal)

    return app
