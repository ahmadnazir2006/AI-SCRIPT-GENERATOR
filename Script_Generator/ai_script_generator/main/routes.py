from markupsafe import Markup
import markdown
from ai_script_generator import model,db,mail
from ai_script_generator.Models import Chat
from flask_login import current_user
from flask import abort







from flask import Blueprint, render_template, request, redirect, url_for, flash
main=Blueprint('main',__name__)


@main.route('/',methods=['GET','POST'])
@main.route('/home',methods=['GET','POST'])
def home():
    chats=[]
    if current_user.is_authenticated:
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
@main.route('/about')
def about():
     posts="Contact us at:\n03004924840\nemail: ahmadnazir9101@gmail.com\nor visit our office in Gulberg "
     return render_template('about.html',posts=posts,title="Ai Script Writer.About")
     


@main.route("/test-403")
def test_403():
    abort(403)  # This forces the 403 error handler to run

# Test Route for 500
@main.route("/test-500")
def test_500():
    abort(500)  # Th