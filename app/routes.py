import base64
import io
from datetime import datetime, timedelta
from collections import Counter
from flask import Blueprint, render_template, flash, redirect, request, url_for, Response, stream_with_context, abort, jsonify
from app.extensions import db

main = Blueprint('main', __name__)
current_user = {'name': 'John'}


@main.route('/')
def index():
    return render_template('index.html')