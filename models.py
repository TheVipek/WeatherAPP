from flask_sqlalchemy import SQLAlchemy

from app import db




class Accounts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(24),unique=True,nullable=False)
    email = db.Column(db.String(32),unique=True,nullable=False)
    password = db.Column(db.String(50),unique=True,nullable=False)
    newsletter = db.Column(db.Boolean(),unique=False,default=False)

    def __init__(self,username,email,password,newsletter):
        self.username = username
        self.email = email
        self.password = password
        self.newsletter = newsletter

