from flask import Flask,Blueprint
from flask.templating import render_template
import logging
import os,sys
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from . import config
from dotenv import load_dotenv




db = SQLAlchemy()

def create_app(config=config.Config):
    app = Flask(__name__,
    static_url_path=""
    )
    
    app.config.from_object(config)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import Accounts
    @login_manager.user_loader
    def load(id):
        return Accounts.query.get(int(id))
    
    from .main import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app


    