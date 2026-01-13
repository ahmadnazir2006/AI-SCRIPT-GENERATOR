import google.generativeai as genai

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv('key.env')


import os
from config import config

from flask_login import login_manager,LoginManager
myapikey=os.getenv('GEMINI_API_KEY')
if myapikey:
            genai.configure(api_key=myapikey)
else:
    print("WARNING: API Key not found in key.env")


bcrypt=Bcrypt()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail = Mail()







try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Error loading Gemini model: {e}")
from ai_script_generator.users.routes import users
from ai_script_generator.chats.routes import chats
from ai_script_generator.main.routes import main
from ai_script_generator.errors.handlers import errors


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.register_blueprint(users)
    app.register_blueprint(chats)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    with app.app_context():
     from ai_script_generator import Models 
     db.create_all()
    return app

