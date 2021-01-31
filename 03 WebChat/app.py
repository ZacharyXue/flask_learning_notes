from flask import Flask,render_template,session,request,redirect,url_for

from setting import config
from libs import db,login_required,loginForm,registerForm
from models import User,Message,Online

from wtforms import SelectField

app = Flask(__name__) 

app.config.from_object(config['development'])

db.init_app(app)


@app.route('/login',methods=['post','get'])
def login():
    form = loginForm()
    message = ''
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validation_password(password):
                session['user'] = user.username
                online = Online(username=user.username)
                db.session.add(online)
                db.session.commit()
                session['message_id'] = 1
                return redirect(url_for('chat'))
            else:
                message = " The password is wrong, please input again" 
        else:
            return redirect(url_for('register'))       
    else:
        print(form.errors)

    return render_template('login.html',message=message,form=form)

@app.route('/logout')
@login_required
def logout():
    username = session['user']
    session.clear()
    user = Online.query.filter(Online.username==username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/register',methods=['post','get'])
def register():
    form = registerForm()
    message = ''
    if form.validate_on_submit():
        name = form.data['name']
        username = form.data['username']
        if validate_username(username):
            return render_template('register.html',message='用户名重复',form=form)
        password = form.data['password']
        password2 = form.data['password2']
        if password != password2:
            return render_template('register.html',message='两次密码输入不一致',form=form)
        married = form.data['married']
        city = form.data['city']
        edu = form.data['edu']
        hobby = '|'.join(form.data['hobby'])
        user = User(name=name,username=username,password=password,married=married,\
            city=city,education=edu,hobby=hobby)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
    else:
        print(form.errors)
    return render_template('register.html',message=message,form=form)


@app.route('/',methods=['post','get'])
@login_required
def chat(online_id=None):
    import json
    start_id = session['message_id']
    end = Message.query.count()
    if request.method == 'POST':
        response = json.loads(request.data)    
        text = response['text']
        listener = response['listener']
        if text:
            message = Message(speaker=session['user'],text=text,listener=listener)
            db.session.add(message)
            db.session.commit()
        messages = [Message.query.get(i).beDict() for i in range(start_id,end+1) if Message.query.get(i)]
        users = [user.username for user in Online.query.all()]
        session['message_id'] = end + 1
        all_messages = {'messages':messages,'users':users}
        return json.dumps(all_messages)

    return render_template('chat.html')

@app.context_processor
def account():
    username = session.get('user')
    return {'username':username}

def validate_username(username):
    return User.query.filter_by(username=username).first()