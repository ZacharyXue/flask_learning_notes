from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String) 
    password = db.Column(db.String)

    # 通过hash相关函数产生密码的加密形式
    def hash_password(self,password):
        self.password = generate_password_hash(password)
    # 对于输入密码和数据库中密码进行比较
    def validation_password(self,password):
        return check_password_hash(self.password,password)

class Article(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    author = db.Column(db.String,default='None')
    date = db.Column(db.DateTime,default=datetime.utcnow)
    # 在从表中定义外键
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))

class Category(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String,unique=True)
    order = db.Column(db.Integer,default=0)
    # 为了建立主表（category）和从表（article）之间关系，在主表中使用relationship定义
    # cascade="delete"使得在删除主表相应分类时该分类下的文章同时删除
    articles = db.relationship("Article",cascade="delete")