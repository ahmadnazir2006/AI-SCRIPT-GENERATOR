from flask import render_template,request,redirect,url_for,flash
from markupsafe import Markup
import markdown
from ai_script_generator import app,model

from ai_script_generator.Form import Signup,Login
from ai_script_generator.Models import User,Chat


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
    form=Signup()
    if form.validate_on_submit():
        
        flash(f"Account created for {form.username.data}!",'success')
        return redirect(url_for('login'))
    return render_template('Signup.html',title='Sign Up',form=form)
@app.route('/Login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validate_on_submit():
      if form.email.data=='ahmadnazir9101@gmail.com' and form.password.data=='123456':
        flash(f'Login Successful for {form.email.data}','success')
        return redirect(url_for('home'))
      else:
         flash(f'Unsuccessful Login.Please check email and password','danger')
    return render_template('Login.html',title='Login',form=form)
