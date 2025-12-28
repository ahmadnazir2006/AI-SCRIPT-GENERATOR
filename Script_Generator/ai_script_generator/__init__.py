import google.generativeai as genai

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app =Flask(__name__)
app.config['SECRET_KEY']='5b5c030b5397b1febbd3a5284ffb2014'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
from ai_script_generator import Routes
