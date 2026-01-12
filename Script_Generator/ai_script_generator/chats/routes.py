from flask import Blueprint, render_template, request, redirect, url_for, flash
from markupsafe import Markup
from ai_script_generator import db
from ai_script_generator.Models import Chat
from flask_login import login_user,logout_user,current_user,login_required
from flask import abort


chats=Blueprint('chats',__name__)


@chats.route('/chat/<int:chat_id>')
@login_required
def view_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        abort(403)  # prevent access to others' chats
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', selected_chat=chat, chats=chats, generated_script=Markup(chat.content))

@chats.route('/new_chat',methods=['GET','POST'])
@login_required
def new_chat():
        return redirect(url_for('chats.home'))
@chats.route('/delete_chat/<int:chat_id>',methods=['POST'])
@login_required
def delete_chat(chat_id):
    chat=Chat.query.get_or_404(chat_id)
    if chat.user_id!=current_user.id:
        abort(403)
    db.session.delete(chat)
    db.session.commit()
    flash('Chat has been deleted!','success')
    return redirect(url_for('chats.home'))
