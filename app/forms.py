# app/forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, IPAddress, Length, URL, EqualTo, ValidationError
from app.models import User