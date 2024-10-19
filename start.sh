#!/bin/bash

# Start Flask app
echo "Starting Flask app..."
gunicorn --bind 0.0.0.0:5000 --log-level info wsgi:app &

# Start Telegram bot
echo "Starting Telegram bot..."
python3 telebot.py &

# Wait for all background processes to finish
wait