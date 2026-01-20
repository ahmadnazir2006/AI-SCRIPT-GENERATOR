from flask import render_template,request,redirect,url_for,flash,request,current_app
from markupsafe import Markup
import markdown
from sqlalchemy import Update
from ai_script_generator import mail,users
from flask_mail import Message
from PIL import Image
import os
import secrets










def send_reset_email(user):
    token=user.reset_password()
    msg=Message('Password Reset Request',sender=current_app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.body=f"""To reset your password,click the following link:
{url_for('users.reset_token',token=token,_external=True)}
The link is valid for 30 minutes.
If you did not make this request then simply ignore this email and no changes will be made."""
    mail.send(msg)

def save_picture(form_picture):
    # 1. Optional: Resize locally before uploading to save bandwidth
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # 2. Upload to Cloudinary
    # We tell Cloudinary to put it in a folder called 'profile_pics'
    upload_result = cloudinary.uploader.upload(
        form_picture, 
        folder="profile_pics",
        transformation=[
            {"width": 125, "height": 125, "crop": "fill"}
        ]
    )
    
    # 3. Return the secure URL provided by Cloudinary
    return upload_result['secure_url']
