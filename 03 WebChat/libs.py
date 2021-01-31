from flask_sqlalchemy import SQLAlchemy
from flask import session,redirect,url_for
from functools import wraps

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,RadioField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired

# 创建数据库对象
db = SQLAlchemy()

# 视图保护装饰器函数
def login_required(func):
    @wraps(func)
    def decorate_nest(*args,**kwargs):
        # user为设置的session参数
        if not 'user' in session:
            return redirect(url_for("login"))
        else:
            return func(*args,**kwargs)
    return decorate_nest

# 登陆表单
class loginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(message='You have to input username')])
    password = PasswordField('password',validators=[DataRequired(message='You have to input password')])
    submit = SubmitField('',render_kw={'value':'submit'})

# 注册表单
class registerForm(FlaskForm):
    name = StringField('name')
    username = StringField('username',validators=[DataRequired(message='You have to input username')])
    password = PasswordField('password',validators=[DataRequired(message='You have to input password')])
    password2 = PasswordField('password2',validators=[DataRequired(message='You have to input password again')])
    married = RadioField('married',choices=[('m','married'),('s','single')])
    city = SelectField('city',choices=[
        ('beijing','Beijing'),
        ('shanghai','Shanghai'),
        ('harbin','Harbin')
    ])
    edu = SelectField('education',choices=[
        ('u','undergraduate'),
        ('g','graduate')
    ])
    hobby = SelectMultipleField('hobby',choices=[
        ('swim','swimming'),
        ('travel','traveling'),
        ('fish','fishing')
    ])
    submit = SubmitField('',render_kw={'value':'submit'})