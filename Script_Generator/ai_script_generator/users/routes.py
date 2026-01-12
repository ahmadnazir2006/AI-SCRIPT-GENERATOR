from flask import Blueprint, render_template, request, redirect, url_for, flash
from ai_script_generator.users.utils import send_reset_email,save_picture
from ai_script_generator.users.forms import Signup,Login,AccountUpdate,RequestReset,ResetPassword
from ai_script_generator.Models import User
from flask_login import login_user,logout_user,current_user,login_required
from ai_script_generator import db,bcrypt










users=Blueprint('users',__name__)

@users.route('/Signup',methods=['GET','POST'])
def signUp():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form=Signup()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created for {form.username.data}!",'success')
        return redirect(url_for('users.login'))
    return render_template('Signup.html',title='Sign Up',form=form)
@users.route('/Login',methods=['GET','POST'])
def login():
     if current_user.is_authenticated:
       return redirect(url_for('users.home'))
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

                return redirect(url_for('main.home'))
        else:
            flash(f'Unsuccessful Login.Please check email and password','danger')
     return render_template('Login.html',title='Login',form=form)
@users.route('/logout')
def logout():
         logout_user()
         return redirect(url_for('users.login'))


@users.route('/account',methods=['GET','POST'])
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
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
                        
    user_image=url_for('static',filename='profile_pic/'+current_user.image)
    return render_template('account.html',title='Account',form=form,image=user_image)


@users.route('/reset_password',methods=['GET','POST'])
def request_reset():
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     form=RequestReset()
     if form.validate_on_submit():
         user=User.query.filter_by(email=form.email.data).first()
         if user is None:
             flash('There is no account with that email. You must register first.','warning')
             return redirect(url_for('users.request_reset'))
         send_reset_email(user)
         flash('An email has been sent with instructions to reset your password.','info')
         return redirect(url_for('users.login'))
     return render_template('request_reset.html',title='Reset Password',form=form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     user=User.verify_reset_token(token)
     if user is None:
            flash('That is an invalid or expired token','warning')
            return redirect(url_for('users.request_reset'))
     form=ResetPassword()
     if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f"Your password has been updated successfully!",'success')
        return redirect(url_for('users.login'))
     return render_template('reset_token.html',title='Reset Password',form=form)
     