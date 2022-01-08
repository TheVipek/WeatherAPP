from io import BytesIO
from typing import Type
from flask.helpers import is_ip, url_for
from flask import flash
from flask_login.utils import login_required, login_user, logout_user
from flask_migrate import current
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from wtforms.fields.simple import SubmitField
from app import app
from app import login_manager
from flask import  render_template,request,make_response,session
from flask_login import LoginManager,current_user
import requests ,ipinfo,os,math,json,sys
from datetime import datetime, timedelta
from models import *


from werkzeug.utils import secure_filename
import re

import configparser
import boto3,botocore









    
 
