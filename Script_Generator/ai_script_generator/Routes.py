from flask import render_template,request,redirect,url_for,flash,request
from markupsafe import Markup
import markdown
from ai_script_generator import app,model,db,bcrypt,login_manager,LoginManager

from ai_script_generator.Form import Signup,Login
from ai_script_generator.Models import User,Chat
from flask_login import login_user,logout_user,current_user,login_required


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        user_prompt=request.form['user_input']
        instruction=f"Write a script about: {user_prompt}" 
        response=model.generate_content(instruction)
        html_text=markdown.markdown(response.text)
        generated = Markup(html_text) 
        return render_template('index.html',generated_script=generated)
    return render_template('index.html')
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
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
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
@app.route('/account')
@login_required

def account():
    form=Login()
    return render_template('account.html',title='Account',form=form)