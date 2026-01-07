from flask import render_template,request,redirect,url_for,flash,request
from markupsafe import Markup
import markdown
from sqlalchemy import Update
from ai_script_generator import app,model,db,bcrypt,login_manager,LoginManager
from PIL import Image
from ai_script_generator.Form import Signup,Login,AccountUpdate,Script
from ai_script_generator.Models import User,Chat
from flask_login import login_user,logout_user,current_user,login_required
import os
import secrets


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


