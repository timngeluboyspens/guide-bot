# wsgi.py
import asyncio
import os
import threading
from app import create_app
from telebot import TelegramBot

app = create_app()

def start_flask_app():
    app.run(port=5000)

def start_telegram_bot():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_USERNAME = "@bambubot"

    # Function to run the bot within its own asyncio event loop
    async def run_bot():
        telegram_bot = TelegramBot(TOKEN, BOT_USERNAME)
        await telegram_bot.run()

    # Use the event loop of the main thread
    asyncio.run(run_bot())

# Start Flask in a separate thread
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()

# Start Telegram bot in the main thread
start_telegram_bot()