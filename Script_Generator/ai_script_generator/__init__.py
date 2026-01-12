import google.generativeai as genai

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv('key.env')


from flask_login import login_manager,LoginManager
myapikey=os.getenv('GEMINI_API_KEY')
if myapikey:
            genai.configure(api_key=myapikey)
else:
    print("WARNING: API Key not found in key.env")

app =Flask(__name__)
app.config['SECRET_KEY']='5b5c030b5397b1febbd3a5284ffb2014'
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USER']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASS']
mail = Mail(app)







model=genai.GenerativeModel('gemini-2.5-flash')

from ai_script_generator import Routes
from ai_script_generator import Models
