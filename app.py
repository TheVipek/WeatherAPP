from flask import Flask
from flask.templating import render_template
from flask import session
import logging
import os
# from wtforms import csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = os.environ.get('session_secret')
# app.secret_key = 'xxxxxx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
from models import *
logging.basicConfig(filename="events.log",level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from views import *

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()