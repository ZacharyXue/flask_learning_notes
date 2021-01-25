from flask import Flask,render_template
from flask import request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # 这里给Flask传入模块名__name__

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  #当数据库数据发生修改时是否进行跟踪
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"  #确定数据库在哪里

db = SQLAlchemy(app)  # 创建数据库对象

# 主页
@app.route("/")  # 路由
def index():
    lists = [
        {"title":"news1","intro":"aaa"},
        {"title":"news2","intro":"bbb"},
        {"title":"news3","intro":"ccc"}
    ]
    return render_template("index.html",newsList=lists)  # 注意后面传入变量：模块内变量=视图函数变量
                                                            # 具体来讲模块内变量是传入HTML的变量，
                                                            # 视图函数变量是该Python函数的变量

class User(db.Model):  # 创建数据类型，这里比较简单只创建了一个包含id和字符串的数据
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)


# 进行数据库操作学习前进行数据库的创建
def createUser():
    words = list('qwertyuiopasdfghjklzxcvbnm')
    
    import random

    for _ in range(100):
        random.shuffle(words)
        username = ''.join(words[:6])
        user = User(username=username)
        db.session.add(user)
    # 为了减少对数据库的访问，所以只在最后提交数据到数据库
    db.session.commit()

# 获取用户列表
@app.route('/userList',methods = ['get'])
def userList():
    users = User.query.all()  # 获得数据库所有的用户
    return render_template('user/user_list.html',users=users)

# 创建用户
@app.route("/login",methods = ['post','get'])  # 后面methods规定了该地址可以接受的返回值类型
def login():
    if request.method == "POST":  # post是指的从表单返回
        # 注意这里使用的是html中的name值
        username = request.form['username']
        user = User(username=username)
        # 添加数据库的两个步骤：
        # 1. add
        # 2. commit
        # 其中commit在所有数据add操作后再进行
        db.session.add(user)
        db.session.commit()
    return render_template("login.html")
    
# 删除用户
@app.route('/user_delete/<int:user_id>')
def deleteUser(user_id):
    # 在html中点击链接后返回带有user_id的网址
    #   即为路由中'/user_delete/<int:user_id>'
    # 然后在视图函数中获得相应参数进行操作
    # 最后重新定位到之前网页，与render_template实现功能不同
    user = User.query.get(user_id)
    db.session.delete(user)  # 删除用户操作
    db.session.commit()
    return redirect(url_for('userList'))  # 

# 用户信息改变
@app.route('/user_edit/<int:user_id>',methods=['get','post'])
def editUser(user_id):    
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['name']
        db.session.commit()
    return render_template('user/edit_user.html',user=user)