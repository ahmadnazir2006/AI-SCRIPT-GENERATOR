from flask import render_template,request,redirect,url_for,flash,request
from markupsafe import Markup
import markdown
from sqlalchemy import Update
from ai_script_generator import app,model,db,bcrypt,login_manager,LoginManager,mail
from flask_mail import Message
from PIL import Image
from ai_script_generator.Form import Signup,Login,AccountUpdate,Script,RequestReset,ResetPassword
from ai_script_generator.Models import User,Chat
from flask_login import login_user,logout_user,current_user,login_required
import os
import secrets
from flask import abort


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    chats=Chat.query.filter_by(user_id=current_user.id).all()
    if request.method=='POST':
            user_prompt=request.form['user_input']
            if user_prompt:

                         instruction=f"Write a script about: {user_prompt}" 
                         try:
                             response=model.generate_content(instruction)
                             html_text=markdown.markdown(response.text)
                             generated = Markup(html_text) 

                             new_chat = Chat(title=user_prompt[:50], 
                             content=generated,
                             author=current_user)
                             db.session.add(new_chat)
                             db.session.commit()
                             chats=Chat.query.filter_by(user_id=current_user.id).all()

                             flash('Your chat has been saved','success')


                             return render_template(('index.html'),generated_script=generated,chats=chats)
                         except Exception as e:
                             return render_template(('index.html'),chats=chats,generated_script=f"Error{str(e)}")
            else:
                flash('Please enter a prompt','warning')

    return render_template('index.html', chats=chats)
@app.route('/about')
def about():
     posts="Contact us at:\n03004924840\nemail: ahmadnazir9101@gmail.com\nor visit our office in Gulberg "
     return render_template('about.html',posts=posts,title="Ai Script Writer.About")
     


@app.route('/Signup',methods=['GET','POST'])
def signUp():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=Signup()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created for {form.username.data}!",'success')
        return redirect(url_for('login'))
    return render_template('Signup.html',title='Sign Up',form=form)
@app.route('/Login',methods=['GET','POST'])
def login():
     if current_user.is_authenticated:
       return redirect(url_for('home'))
     form=Login()
     if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember_me.data)
            
            next_page=request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                flash(f'Login Successful for {form.email.data}','success')

                return redirect(url_for('home'))
        else:
            flash(f'Unsuccessful Login.Please check email and password','danger')
     return render_template('Login.html',title='Login',form=form)
@app.route('/logout')
def logout():
         logout_user()
         return redirect(url_for('login'))
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

@app.route('/account',methods=['GET','POST'])

@login_required

def account():
    form=AccountUpdate()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
                        
    user_image=url_for('static',filename='profile_pic/'+current_user.image)
    return render_template('account.html',title='Account',form=form,image=user_image)
@app.route('/chat/<int:chat_id>')
@login_required
def view_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        abort(403)  # prevent access to others' chats
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', selected_chat=chat, chats=chats, generated_script=Markup(chat.content))

@app.route('/new_chat',methods=['GET','POST'])
@login_required
def new_chat():
        return redirect(url_for('home'))
@app.route('/delete_chat/<int:chat_id>',methods=['POST'])
@login_required
def delete_chat(chat_id):
    chat=Chat.query.get_or_404(chat_id)
    if chat.user_id!=current_user.id:
        abort(403)
    db.session.delete(chat)
    db.session.commit()
    flash('Chat has been deleted!','success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token=user.reset_password()
    msg=Message('Password Reset Request',sender=app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.body=f"""To reset your password,click the following link:
{url_for('reset_token',token=token,_external=True)}
The link is valid for 30 minutes.
If you did not make this request then simply ignore this email and no changes will be made."""
    mail.send(msg)
@app.route('/reset_password',methods=['GET','POST'])
def request_reset():
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     form=RequestReset()
     if form.validate_on_submit():
         user=User.query.filter_by(email=form.email.data).first()
         if user is None:
             flash('There is no account with that email. You must register first.','warning')
             return redirect(url_for('request_reset'))
         send_reset_email(user)
         flash('An email has been sent with instructions to reset your password.','info')
         return redirect(url_for('login'))
     return render_template('request_reset.html',title='Reset Password',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     user=User.verify_reset_token(token)
     if user is None:
            flash('That is an invalid or expired token','warning')
            return redirect(url_for('reset_password'))
     form=ResetPassword()
     if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f"Your password has been updated successfully!",'success')
        return redirect(url_for('login'))
     return render_template('reset_token.html',title='Reset Password',form=form)
     