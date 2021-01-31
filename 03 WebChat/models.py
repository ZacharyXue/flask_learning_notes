from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,unique=True) 
    name = db.Column(db.String)
    password = db.Column(db.String)
    married = db.Column(db.String)
    city = db.Column(db.String)
    education = db.Column(db.String)
    hobby = db.Column(db.String)
    message = db.relationship("Message",cascade="delete")
    online = db.relationship("Online",cascade="delete")

    def hash_password(self,password):
        self.password = generate_password_hash(password)
    def validation_password(self,password):
        return check_password_hash(self.password,password)

class Message(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    speaker = db.Column(db.String,db.ForeignKey('user.username'))
    listener = db.Column(db.String)
    text = db.Column(db.String)
    date = db.Column(db.String,default=str(datetime.now()))

    def beDict(self):
        return {'id':self.id,'speaker':self.speaker,'listener':self.listener,\
            'text':self.text,'date':self.date}

class Online(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,db.ForeignKey('user.username'))