from flask import Blueprint,render_template
from flask import redirect,url_for,request
import sys 
sys.path.append('..')
from models import Article,Category
from app import db
from libs import login_required

article_app = Blueprint("article_app",__name__)

@article_app.route('/list',methods=['get','post'])
def articleList():
    if request.method=='POST':
        field,name = request.form['field'],request.form['name']
        if field == 'id':
            condition = Article.id.like('%{}%'.format(name))
        else:
            condition = Article.title.like('%{}%'.format(name))
        articles = Article.query.filter(condition).all()
    else:
        articles = Article.query.all()
    return render_template('article/article_list.html',articles=articles)

@article_app.route('/view/<int:article_id>')
def view(article_id):
    article = Article.query.get(article_id)
    # 查询不到时返回文章列表
    if not article:
        return redirect(url_for('article_app.articleList'))
    return render_template('article/detail.html',article=article)

@article_app.route('/delete/<int:article_id>')
@login_required  # 设置视图函数保护
def delete(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('article_app.articleList'))

@article_app.route('/edit/<int:article_id>',methods=['get','post'])
@login_required
def edit(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        # article.author = 
        article.content = request.form['content']
        article.category_id = request.form['category']
        db.session.commit()
    return render_template('article/edit.html',article=article)

@article_app.route('/post',methods=['get','post'])
@login_required
def post():
    if request.method == 'POST':
        article_title = request.form['title']
        article_content = request.form['content']
        article_category = request.form['category']
        article = Article(title=article_title,content=article_content,category_id=article_category)
        db.session.add(article)
        db.session.commit()
    return render_template('article/post.html')

##### category #####

@article_app.route('/add_category',methods=['get','post'])
@login_required
def addCategory():
    message = ''
    if request.method == "POST":
        name = request.form['name']
        order = request.form['order']
        category = Category(name=name,order=order)
        # 因为models中name字段设置了unique，存在添加失败可能
        try:
            db.session.add(category)
            db.session.commit()
            message = name + " is added successfully"
        except Exception as e:
            message = "There is some problems: "+ str(e)
            db.session.rollback()
    return render_template('category/add.html',message=message)

@article_app.route('/category')
def categoryList():

    # need a search function
    
    # 按降序排列  
    categorys = Category.query.order_by(Category.order.desc()).all()
    return render_template('/category/list.html',categorys=categorys)

@article_app.route('/delete_category/<int:id>')
@login_required
def deleteCategory(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('article_app.categoryList'))

@article_app.route('/edit_category/<int:id>',methods=['get','post'])
@login_required
def editCategory(id):
    category = Category.query.get(id)
    if request.method == "POST":
        category.name = request.form['name']
        category.order = request.form['order']
        db.session.commit()
    return render_template('category/edit.html',category=category)

@article_app.route('/category_view/<int:category_id>')
def articleListByCategory(category_id):
    res = Article.query.filter_by(category_id=category_id).all()
    return render_template('article/article_list.html',articles=res)