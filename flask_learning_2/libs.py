from flask_sqlalchemy import SQLAlchemy
from flask import session,redirect,url_for
from functools import wraps

# 创建数据库对象
db = SQLAlchemy()

# 视图保护装饰器函数
def login_required(func):
    @wraps(func)
    def decorate_nest(*args,**kwargs):
        # user为设置的session参数
        if not 'user' in session:
            return redirect(url_for("user_app.login"))
        else:
            return func(*args,**kwargs)
    return decorate_nest