from datetime import timedelta
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://myuser:mypassword@localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TEMPLATE_AUTO_RELOAD = True 
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = '/tmp/flask_session'
    SESSION_FILE_THRESHOLD = 500
    SESSION_FILE_MODE = 384
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # SESSION_TYPE = 'redis'
    # SESSION_PERMANENT = True
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=0)
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
