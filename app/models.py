from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db




class Accounts(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(24),nullable=False)
    email = db.Column(db.String(32),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    newsletter = db.Column(db.Boolean(),default=False)
    # imagep = db.Column(db.String(100),unique=False,nullable=True)
    def __init__(self,username,email,password,newsletter):
        self.username = username
        self.email = email
        self.password = password
        self.newsletter = newsletter
        # self.imagep = imagep

class UsernameExpire(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    expires = db.Column(db.DateTime,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey(Accounts.id),nullable=False)

    def __init__(self,expires,user_id):
        self.expires = expires
        self.user_id = user_id
class UserImage(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey(Accounts.id),nullable=False)
    user_profile = db.Column(db.Text,nullable=True)
    
    def __init__(self,user_profile,user_id):
        self.user_profile = user_profile
        self.user_id = user_id
# class UserImage(UserMixin,db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     image = image
