from flask import render_template,request,redirect,url_for,flash,request
from markupsafe import Markup
import markdown
from sqlalchemy import Update
from ai_script_generator import mail,app,users
from flask_mail import Message
from PIL import Image
import os
import secrets










def send_reset_email(user):
    token=user.reset_password()
    msg=Message('Password Reset Request',sender=app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.body=f"""To reset your password,click the following link:
{url_for('users.reset_token',token=token,_external=True)}
The link is valid for 30 minutes.
If you did not make this request then simply ignore this email and no changes will be made."""
    mail.send(msg)

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pic',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn