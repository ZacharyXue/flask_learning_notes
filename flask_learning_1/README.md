
- [配置记录](#配置记录)
  - [虚拟环境的创建](#虚拟环境的创建)
  - [`flask`的安装使用](#flask的安装使用)
- [功能实现](#功能实现)
  - [数据库初始化](#数据库初始化)
  - [数据库创建](#数据库创建)
  - [数据库操作](#数据库操作)
    - [路由](#路由)
    - [`query`方法](#query方法)
    - [`render_template`函数](#render_template函数)
    - [模板语法](#模板语法)
    - [数据的查增删改](#数据的查增删改)

## 配置记录

### 虚拟环境的创建

在使用flask建站时选择在虚拟环境下进行，因为这样可以与其他模块隔离以免存在版本冲突，这里使用的是 pipenv 模块。

1. 创建目录、进入目录 
2. 配置虚拟环境目录
    - Linux： `export PIPENV_VENV_IN_PROJECT=1`
    - Windows: `set PIPENV_VENV_IN_PROJECT=1`（项目不能放在C盘）
    
    这一步的意义并不是很清楚，后来自己在重新创建虚拟环境时没有执行这一步也是可以行得通的，从[这篇文章](https://www.cnblogs.com/ameile/p/10059272.html)来看应该是虚拟环境的储存地址。后面整理代码删除该部分时发现`.env`文件很大，应该可以印证这一点。
3. 创建虚拟环境 `pipenv install`，之后激活环境时使用` pipenv shell`。

创建好的环境包含[Pipfile](Pipfile)和[Pipfile.lock](Pipfile.lock),前者为依赖包文件表后者为依赖包详细版本信息。

### `flask`的安装使用

安装:

```shell
pipenv install flask
```

运行命令：
```shell
flask run [--host *** ---port ***]
```
进入运行环境：
```shell
flask shell
```
为在`flask`运行时仍可以看到代码修改状态，可进行配置:
```shell
export FLASK_ENV=development
export FLASK_DEBUG=debug
```
要注意的是`flask`对于文件放置的一些特殊要求：
- html文件默认应放于templates目录；
- CSS、JavaScript文件默认应放于static目录。


## 功能实现

在初步学习`flask`模块时初步实现了数据库创建、调用、修改和删除，这里使用 `flask_sqlalchemy`模块来实现基本的数据库功能。

### 数据库初始化

首先是在[app.py](app.py)中创建数据库实例：
```python
app = Flask(__name__) # 这里给Flask传入模块名__name__

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  #当数据库数据发生修改时是否进行跟踪
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"  #确定数据库在哪里

db = SQLAlchemy(app)  # 创建数据库对象
```
同时需要创建要使用到的数据模型：
```Python
class User(db.Model):  # 创建数据类型
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)
```
之后需要创建数据表：
```shell
# flask shell
>>> from app import db
>>> db.create_all()
```

### 数据库创建

在`flask_sqlalchemy`模块中对于数据库操作较为简单，创建步骤如下：
```Python
user = User(***)  # 实例化
db.session.add(user)  # 添加数据
db.session.commit()  #提交数据
```
在[这里](app.py)，使用函数批量创建用户从而方便后面进行数据库操作学习。

### 数据库操作

#### 路由

在需要界面访问的视图函数前应该先使用`app.route`进行装饰从而提供访问路径（路由），此处可能传入的值为 `methods`(数组)，可以为`get`或者`post`或者二者都包含。

关于路由要注意的是利用`get`获得用户输入值时路由的地址书写方式：
```python
@app.route('/user_edit/<int:user_id>',methods=['get','post'])
```
视图函数则可以直接通过函数变量传入`get`获得值。

#### `query`方法

要进行数据查询时需要使用模型的`query`方法进行，具体使用方法应该查询官网，这里列出简单的几个方法：
|查询方法|说明|
|:-:|:-|
|`all()`|获得所有记录|
|`first()`|获得第一条记录，找不到返回 `None`|
|`one()`|返回唯一一条记录，如果存在多条或者没有则报错|
|`get(id)`|传入主键`id`，返回与主键匹配的记录，没有则返回`None`|
|`count()`|返回查询结果总数|
|`one_or_none()`|功能与`one()`相同，只是结果不唯一时返回 `None`|

#### `render_template`函数

在视图函数中使用`render_template`函数可以渲染模板，通俗一点讲就是将视图函数中的数据显示在指定的网页中。

这里的输入除去指定网页的HTML之外，还有相应的传入变量，格式为`模块内变量=视图函数变量`。

#### 模板语法

模板语法是在HTML文件中调用视图函数数据时使用的语法。

基础语法：
- `{{  }}`：变量
- `{% %}`：语句
- `{# #}`：注释

关于**模板继承**可以看[index.html](templates/index.html)与其他几个HTML文件之间的写法。简单说，模板中将其他HTML可能修改部分使用`{% block block_name %} ... {% endblock%}`包裹起来，然后在其他HTML开始注明`{% extends "index.html" %}`,然后只需要写必要的`block`。

#### 数据的查增删改

- 数据的查询使用上面[`query`](#query方法)相关方法就可以实现；
- 数据的增加利用上面[数据库创建](#数据库创建)中的`db.session.add()`可以实现；
- 数据的删除使用`db.session.delete()`可以实现；
- 数据的修改先获得相应数据的主键，然后便可以对相关元素进行修改。
