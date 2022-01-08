import os 
from datetime import timedelta
class Config(object):
    SQLALCHEMY_DATABASE_URI='sqlite:///users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('app_key')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    
