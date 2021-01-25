from flask import Flask,render_template,session

from libs import db
from models import Category
from views.users import user_app
from views.articles import article_app
from views.upload import upload_app

from flask_migrate import Migrate

app = Flask(__name__) 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db" 
# 设置上传中允许的文件类型
app.config['ALLOWED_UPLOAD_TYPE'] = ['image/jpg','image/png','image/jpeg'] 

db.init_app(app)  # 数据库对象db的初始化
# 添加路由到 app 对象
app.register_blueprint(user_app,url_prefix="/user")
app.register_blueprint(article_app,url_prefix="/article")
app.register_blueprint(upload_app,url_prefix="/upload")

# 该属性是为了使用session而设置的密钥
app.secret_key = '123456'

@app.route('/')
def index():
    return render_template('index.html')

# 上下文处理器：在所有模板中都可以使用
@app.context_processor
def account():
    username = session.get('user')
    return {'username':username}

@app.context_processor
def getCategory():
    categorys = Category.query.all()
    return {'categorys':categorys}

migrate = Migrate(app,db,render_as_batch=True) 
# render_as_batch，记得是不加的时候改数据库字段会遇到问题