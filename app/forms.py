from wtforms import Form,BooleanField,StringField,PasswordField,EmailField,validators,FileField,SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField,FileRequired
from wtforms.validators import Regexp, ValidationError
from PIL import Image
import io
from werkzeug.security import generate_password_hash,check_password_hash
from .models import Accounts


class RegistrationForm(Form):
    """
    Form used while person is trying to register
    """
    username = StringField('Username',validators=[validators.length(min=8,max=24),validators.DataRequired()])
    password = PasswordField('Password',validators=[validators.length(min=8,max=32),
    validators.EqualTo('re_password','Make sure passwords are the same'),validators.DataRequired()])
    re_password = PasswordField('Repeat Password')
    email = EmailField('E-mail',validators=[validators.length(max=50),
    validators.EqualTo('re_email','Make sure e-mail is the same'),validators.DataRequired()])
    re_email =EmailField('Repeat E-mail')
    newsletter = BooleanField('Want join to newsletter? (Informations about updates in first place!)')
    submit = SubmitField('Register')

class LoginForm(Form):
    """
    Form used while user is trying to login
    """
    username =StringField('Username',validators=[validators.DataRequired()])
    password = PasswordField('Password',validators=[validators.DataRequired()])
    Remember_Me=BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class FileUpload(FlaskForm):
    image = FileField(label="",validators=[
    FileRequired(message="You didn't chosen image"),
    FileAllowed(['pdf','jpeg','png','jpg'],message="Only JPG,JPEG and PNG format is allowed.")
    ],description="File must be 200x200 and in JPG,JPEG or PNG format."
    )
    upload = SubmitField('Upload',name="upload",default=False)

    def SizeCheck(self,filename):
        file_content_stream = io.BytesIO(filename)
        img = Image.open(file_content_stream)
        if img.width > 200 or img.height > 200:
            self.image.errors +=(ValidationError('width and height must be 200 or lower'),)

class UsernameForm(Form):
    """
    Form used while user is already logged in and wants to change his username
    """
    old_username = StringField('Username')
    new_username = StringField('New Username',validators=[
        validators.length(min=8,max=24 ,message="Username must have at least 8 characters."),
        validators.regexp('^[A-Za-z]{3,}',message="Username must start with at least 3 letters")
    ])
    change_profile = SubmitField('ChangeProfile',name="profile",default=False)

    def IfUsernameExists(self,new_username):
        """
        check's if new_username exists in database
        """
        new_username = self.new_username.data
        if Accounts.query.filter_by(username=new_username).first():
            return True
        return False

class PasswordForm(Form):
    """
    Form used while user wants to change his password
    """
    old_password = PasswordField('Password')
    new_password = PasswordField('New Password',validators=[validators.length(min=8,max=32)])
    change_password = SubmitField('ChangePassword',name="password",default=False)


    def CheckPassword(self,hash):
        """
        check's whether old password is good (by comparing string with already set in database hash)
        """
        old_password = self.old_password.data
        new_password = self.new_password.data
        if check_password_hash(hash,old_password):
            return True
        # old_password.errors += ValidationError("Check if current password is right and new is not the same as old")
        # new_password.errors += ValidationError("Check if current password is right and new is not the same as old")
        return False

    def PasswordChange(self):
        """
        checks if new password is different than old.
        """
        old_password = self.old_password.data
        new_password = self.new_password.data

        if new_password != old_password:
            return True
        # old_password.errors += ValidationError("Check if current password is right and new is not the same as old")
        # new_password.errors += ValidationError("Check if current password is right and new is not the same as old")
        return False
    def GenerateNewPassword(self):
        """
        Generate new password hash for security reasons.
        """
        new_password = self.new_password.data
        return generate_password_hash(new_password)

class EmailForm(Form):
    """
    Form used while user wants to change his email
    """
    old_email = EmailField('E-mail')
    new_email = EmailField('New E-mail',validators=[validators.length(max=50)])
    change_email = SubmitField('ChangeEmail',name="email",default=False)

    def CheckEmail(self,user_email):
        """
        checks if old email is correct
        """
        old_email=self.old_email.data
        if old_email == user_email:
            return True
        return False 

    def IfEmailExists(self,new_email):
        """
        check's if email exists in database
        """
        new_email = self.new_email.data
        if Accounts.query.filter_by(email=new_email).first():
            return True
        return False

class DeleteAccount(Form):
    """
    Form used when user wants to delete his account.
    """
    delete_button = SubmitField('DeleteAccount')
