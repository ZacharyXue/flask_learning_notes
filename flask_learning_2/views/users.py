from flask import Blueprint,render_template
from flask import redirect,url_for,request,session
import sys 
sys.path.append('..')
from models import User
from app import db
from libs import login_required

# 创建Blueprint对象
user_app = Blueprint("user_app",__name__)

@user_app.route('/list',methods=['get','post'])
@login_required
def usersList():  # 上一行添加了视图保护装饰器
    if request.method=='POST':
        field,name = request.form['field'],request.form['name']
        if field == 'id':  # 判断搜索字段
            condition = User.id.like('%{}%'.format(name))  # 创建搜索条件
        else:
            condition = User.username.like('%{}%'.format(name))
        users = User.query.filter(condition).all()
    else:
        users = User.query.all()
        # 分页显示
        # page = request.args.get('page')
        # users = User.query.paginate(int(page or '1'),10)
    return render_template('user/user_list.html',users=users)
    # return render_template('user/user_list.html',users=users.items,\
    #     pages=users.pages,total=users.total,pageList=users.iter_pages())

@user_app.route('/register',methods=['get','post'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        if validate_username(username):
            return render_template('user/register.html',message='用户名重复')
        password = request.form['password']
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
    return render_template('user/register.html',message='注册成功')

@user_app.route('/login',methods=['get','post'])
def login():
    message = ''
    if request.method=='POST':
        username = request.form['name']
        password = request.form['password']
        # 查询数据库中该用户
        user = User.query.filter_by(username=username).first()
        if user and user.validation_password(password):
            session['user'] = user.username  # 设置session中键值对
            return redirect(url_for('index'))  # 返回主页
        else:
            message = 'The password is wrong'
    return render_template('/user/login.html',message=message)

@user_app.route('/delete/<int:user_id>')
@login_required
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_app.usersList'))

@user_app.route('/edit/<int:user_id>',methods=['get','post'])
@login_required
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['name']
        db.session.commit()
    return render_template('user/edit_user.html',user=user)

def validate_username(username):
    return User.query.filter_by(username=username).first()