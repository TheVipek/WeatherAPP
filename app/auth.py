from flask import Blueprint,flash,redirect,render_template,request,session,url_for
from flask_login import current_user,login_user,logout_user,login_required
from .forms import RegistrationForm,LoginForm,FileUpload,UsernameForm,PasswordForm,EmailForm,DeleteAccount
from app import db
from datetime import datetime,timedelta
from .models import Accounts,UsernameExpire,UserImage
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from .s3_handler import *
import os
from PIL import Image
auth = Blueprint('auth',__name__)

from .main import base,success

@auth.route('/login' ,methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.base'))
    # users = Accounts.query.all()
    # for user in users:
    #     db.session.delete(user)
    #     db.session.commit()
    # user_expires = UsernameExpire.query.all()

    # for user in user_expires:
    #     db.session.delete(user)
    #     db.session.commit()

    # user_image = UserImage.query.all()

    # for user in user_image:
    #     db.session.delete(user)
    #     db.session.commit()
    form = LoginForm(request.form)
    print(form.data)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            users = Accounts.query.all()
            for user in users:
                if username == user.username:
                    fetch = Accounts.query.filter_by(username=username).first()
                    if check_password_hash(fetch.password,password):
                        login_user(fetch,remember=form.Remember_Me.data)
                        flash('Sucessfully logged in!')
                        return redirect(url_for('main.base'))
            else:
                flash('Username or password is wrong.')
                return render_template('login-system/login.html',form=form)
                
    return render_template('login-system/login.html',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.base'))

@auth.route('/register',methods=['POST','GET'])
def register():
    registration = RegistrationForm(request.form)
    if request.method == "POST":
        print('post')
        if registration.validate():
            username = registration.username.data
            email = registration.email.data
            print(username ,email)
            if Accounts.query.filter_by(username=username).first():
                print('exists')
                flash('Username is already used.')
                return render_template('login-system/register.html',form=registration)
            if Accounts.query.filter_by(email=email).first():
                print('email')
                flash('Email is already used.')
                return render_template('login-system/register.html',form=registration)
            password_hash = generate_password_hash(registration.password.data)
            newsletter = registration.newsletter.data
            user = Accounts(username=username,email=email,password=password_hash,newsletter=newsletter)
            db.session.add(user)
            db.session.commit()
            print(user.id)
            now =datetime.now()
            expires = now + timedelta(minutes=10)
            username_expires = UsernameExpire(user_id=user.id,expires=expires)
            db.session.add(username_expires)
            user_image = UserImage(user_profile="0244493818.png",user_id=user.id)
            db.session.add(user_image)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for('main.success'))
                
    return render_template('login-system/register.html',form = registration)
@auth.route('/settings',methods=["GET","POST"])
@login_required
def dashboard():
    if current_user.is_authenticated:
        user_account = Accounts.query.filter_by(id=current_user.id).first()
        user_expire = UsernameExpire.query.filter_by(user_id=current_user.id).first()
        user_image = UserImage.query.filter_by(user_id=current_user.id).first()
        user_profile = UsernameForm(request.form)
        user_password = PasswordForm(request.form)
        user_email = EmailForm(request.form)
        user_delete = DeleteAccount(request.form)
        file_upload = FileUpload()

        img_name= UserImage.query.filter_by(id=current_user.id).first().user_profile
        region = os.environ.get('region')
        bucket=os.environ.get('s3_bucket')
        img_url=f"https://{bucket}.s3.{region}.amazonaws.com/{img_name}"

        
        if request.method== "POST":      
            print('post')
            #If user clicks Upload
            if file_upload.upload.data == True:
                print(file_upload.data)
                #1.get file 
                if file_upload.validate() == True:
                    f = file_upload.image.data
                    print(f)
                    if f:

                        # pass save filename
                        f_name = secure_filename(f.filename)
                        
                        f.seek(0)
                        file_content =f.read()

                        file_upload.SizeCheck(filename=file_content)
                        
                        s3 = boto3.client(
                            "s3",
                            aws_access_key_id=os.environ.get('aws_access_key_id'),
                            aws_secret_access_key=os.environ.get('aws_secret_access_key')
                        )   
                    

                        s3.put_object(
                            Bucket=os.environ.get('s3_bucket'),
                            Key=f_name,
                            Body=file_content
                        )
                        items = s3.list_objects(Bucket=os.environ.get('s3_bucket'))
                        print(items['Contents'])
                        for item in items['Contents']:
                            print(item['Key'])

            if user_profile.change_profile.data == True:
                print('user button')
        
                if user_profile.validate() == True:
                    print(current_user.username)
                    if user_profile.IfUsernameExists(new_username=user_profile.new_username.data) == False:
                        user_account = Accounts.query.filter_by(id=current_user.id).first()
                        username_expire = UsernameExpire.query.filter_by(id=current_user.id).first()
                        print(username_expire.expires)
                        if username_expire.expires < datetime.now():
                            user_account.username = user_profile.new_username.data
                            username_expire.expires = datetime.now()+timedelta(minutes=10)
                            print(username_expire.expires)
                            db.session.commit()
                            flash('Sucessfully changed username.')


                        else:
                            flash(f'You cant change your username until {username_expire.expires.strftime("%m/%d/%Y")}',)
                        user_profile.new_username.data = ""
                    else:
                        flash('Username already exists.')
                        user_profile.new_username.data = ""


            #If user clicks ChangePassword

            if user_password.change_password.data == True:
                if user_password.validate() == True:
                    if user_password.CheckPassword(current_user.password):
                        if user_password.PasswordChange():
                            user_account = Accounts.query.filter_by(id=current_user.id).first()
                            user_account.password = user_password.GenerateNewPassword()
                            print(user_password.old_password.data)
                            print(user_password.new_password.data)
                            db.session.commit()
                            flash('Sucessfuly changed password')
                        else:
                            flash('Check if current password is right and new is not the same as old')
                    else:
                        flash('Check if current password is right and new is not the same as old')
                        
            #If user clicks ChangeEmail
            if user_email.change_email.data == True:
                print('emai lclick')
                if user_email.validate() == True:
                    print(current_user.email)
                    if user_email.CheckEmail(current_user.email) == True:
                        if user_email.IfEmailExists(user_email.new_email.data) == False:
                            user_account = Accounts.query.filter_by(id=current_user.id).first()
                            user_account.email = user_email.new_email.data
                            print(user_email.old_email.data)
                            print(user_email.new_email.data)
                            db.session.commit()
                            user_email.old_email.data =""
                            user_email.new_email.data =""
                            flash('Sucessfuly changed email')
                        else:
                            flash('Email is already used')
                    else:
                        flash('Check if current email is good')

            #If user clicks DeleteAccount
            if user_delete.delete_button.data == True:
                user_account = Accounts.query.filter_by(id=current_user.id).first()
                user_expire = UsernameExpire.query.filter_by(user_id=current_user.id).first()
                user_image = UsernameExpire.query.filter_by(user_id=current_user.id).first()
                print(user_account,user_expire,user_image)
                db.session.delete(user_account)
                db.session.delete(user_expire)
                db.session.delete(user_image)
                db.session.commit()
                flash('Account has been deleted')
                return redirect(url_for('main.base'))
        user_profile.new_username.data = ""
        return render_template("login-system/settings.html",profile_form = user_profile,file_upload=file_upload,password_form=user_password,email_form = user_email,delete_form = user_delete,now_user=current_user.username,img=img_url)

