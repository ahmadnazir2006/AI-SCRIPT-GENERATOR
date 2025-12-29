import google.generativeai as genai

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app =Flask(__name__)
app.config['SECRET_KEY']='5b5c030b5397b1febbd3a5284ffb2014'
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

model=genai.GenerativeModel('gemini-2.5-flash')

from ai_script_generator import Routes
