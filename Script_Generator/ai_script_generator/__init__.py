import google.generativeai as genai

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
from flask_login import login_manager,LoginManager


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app =Flask(__name__)
app.config['SECRET_KEY']='5b5c030b5397b1febbd3a5284ffb2014'
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

model=genai.GenerativeModel('gemini-2.5-flash')

from ai_script_generator import Routes
from ai_script_generator import Models
