# wsgi.py
import asyncio
import os
import signal
import threading
from app import create_app
from app.telegram_bot import TelegramBot

bot = None

def polling_bot():
    global bot

    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_USERNAME = "@bambubot"

    print('Starting bot...')
    bot = TelegramBot(TOKEN, BOT_USERNAME)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.run())

def handle_shutdown_signal(signal, frame):
    global bot

    if bot is not None:
        bot.stop()

    print('Shutting down the server...')
    os._exit(0)

if __name__ == "__main__":
    app = create_app()

    # Run the bot in the main thread
    bot_thread = threading.Thread(target=polling_bot, name="TelegramBot")
    bot_thread.start()

    # Run the Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    flask_thread.start()

    # Capture SIGINT (Ctrl+C) and SIGTERM signals
    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    flask_thread.join()
    bot_thread.join()