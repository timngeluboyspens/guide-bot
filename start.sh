#!/bin/bash

# Start Flask app
echo "Starting Flask app..."
gunicorn --workers 2 --timeout 120 --bind 0.0.0.0:5000 --log-level info wsgi:app &

# Start Telegram bot
echo "Starting Telegram bot..."
python3 telebot.py &

# Wait for all background processes to finish
wait