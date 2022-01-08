# from flask import Flask
# from flask.templating import render_template
# from datetime import timedelta
# from flask import session
# import logging
import os 
from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager

# app = Flask(__name__)
# app.secret_key =  os.environ.get('app_key')
# app.permanent_session_lifetime = timedelta(minutes=60)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.init_app(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# @login_manager.user_loader
# def load(id):
#     return Accounts.query.get(int(id))
# logging.basicConfig(filename="events.log",level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# from models import *
# from views import *

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)