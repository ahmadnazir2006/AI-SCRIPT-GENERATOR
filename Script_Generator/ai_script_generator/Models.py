from datetime import datetime
from ai_script_generator import db,login_manager
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app 


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    image=db.Column(db.String(260),nullable=False,default='default.jpg')
    chat=db.relationship('Chat',backref='author',lazy=True)



    def reset_password(self):
        s=Serializer(current_app.config['SECRET_KEY'],salt='email-confirm')
        return s.dumps({'user_id':self.id})
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'],salt='email-confirm')
        try:
           user_id=s.loads(token,max_age=1800)['user_id']
        except(BadSignature,SignatureExpired):
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"





class Chat(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    title=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
       return f"Chat('{self.title}','{self.content}','{self.date}','{self.post}')"
@login_manager.user_loader
def loaduser(user_id):
    return User.query.get(int(user_id))
