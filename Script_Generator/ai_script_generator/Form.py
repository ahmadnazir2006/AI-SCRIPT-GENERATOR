from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class Signup(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),Length(min=6,max=20),EqualTo('password')])
    submit=SubmitField('Sign Up')
class Login(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Login')