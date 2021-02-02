- [代码重构](#代码重构)
  - [数据库对象处理](#数据库对象处理)
  - [路由处理](#路由处理)
- [添加用户功能](#添加用户功能)
  - [数据库操作](#数据库操作)
    - [多模型间关联](#多模型间关联)
    - [更新数据库](#更新数据库)
  - [访问受限的实现](#访问受限的实现)
    - [`session`模块](#session模块)
    - [上下文处理器](#上下文处理器)
    - [视图保护](#视图保护)
  - [其他](#其他)
    - [密码哈希化](#密码哈希化)
    - [分页显示](#分页显示)
    - [`ckeditor`](#ckeditor)
- [需要继续学习的地方](#需要继续学习的地方)

# 代码重构

之前应用 `flask` 模块进行了简单的应用，实现了初步的网页上数据的更改，但是实际使用过程中不可能将所有的功能都集中在`app.py`一个文件中，所以需要对之前代码进行重构，使其结构更加清晰。

## 数据库对象处理

之前的代码中数据库对象的初始化为 `db = SQLAlchemy(app)`，在代码重构中尝试将该部分放入专门的辅助库中，这时便不能在创建实例的时候初始化，在`app.py`中初始化`SQLAlchemy`对象 `db`如下：
```Python
from libs import db
db.init_app(app)
```

## 路由处理

`Blueprint`模块可以在 `app` 实例没有创建前编写好路由，然后在创建 `app` 实例时使用 `register_blueprint()` 函数将路由添加到响应的。

以 `views/articles.py` 为例：
1. 在相应模块中编写路由相关程序
```Python
article_app = Blueprint("article_app",__name__)

@article_app.route('/list',methods=['get','post'])
def articleList():
...
```
2. 在 `app` 实例中注册该路由
```Python
app.register_blueprint(user_app,url_prefix="/user")
```

注意此时对于视图函数引用是不是直接书写视图函数名：
```Python
    return redirect(url_for('article_app.articleList'))
```

# 添加用户功能

之前没有用户登录功能，在进一步学习中给用户增加了密码，增加了非登录用户访问受限、用户密码哈希化等。

## 数据库操作

### 多模型间关联

在现在建立的模型中文章模型和分类模型是有关联的，这时候涉及主表和从表：

- 主表：自己的主键或者唯一键为其他表的外键
- 从表：自己的某个字段值为另一个表的主键字段值

文章中的分类字段为分类模型中的主键，因此

- 在文章模型中对分类字段定义：
    ```Python
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))
    ```
- 在分类模型中建立主表和从表之间关联：
    ```Python
    articles = db.relationship("Article",cascade="delete")
    ```
    其中，`cascade="delete"`使得在删除主表相应分类时该分类下的文章同时删除。


### 更新数据库

在创建数据库后对于数据库类型进行更改，此时需要使用 `flask_migrate`模块对数据库进行更新。

当然假如不保存数据只更新数据库模型，可以将数据库文件删除然后重新创建，亲试可以……

1. 安装`flask_migrate`数据库管理插件，然后在 `app.py`中创建实例：
    ```Python
    from flask_migrate import Migrate

    migrate = Migrate(app,db,render_as_batch=True)  
    ```
    其中，`render_as_batch=True`增加了对于修改字段的支持。
2. 在命令行中执行命令：
    ```shell
    flask db init
    flask db migrate -m "***"
    flask db upgrade
    ```

## 访问受限的实现

### `session`模块

要**记录用户的登录状态**，就要使用到cookie，但是因为cookie对象可以被浏览器访问修改，所以对于用户登录来说不够安全，所以这里使用`session`模块（对cookie进行加密）。

在服务器端`session`使用密钥进行加密，故在`app.py`中需要设置密钥：
```Python
app.secret_key = '123456'
```
然后便可以进行`session`键值对的设置，如 `users.py`中
```Python
session['user'] = user.username
```

### 上下文处理器

为了使得登录后网页显示例如文章修改、添加等入口，需要在HTML中可以**获得 `session` 中的用户信息**。

这部分内容可以从服务器获得，为了使得全局可以获得相关信息，则需要使用上下文处理器：
```Python
# app.py
@app.context_processor
def account():
    username = session.get('user')
    return {'username':username}
```
在服务器使用上下文处理器后在HTML使用模板语言即可控制元素的显示与否：
```HTML
<!-- index.html -->
{% if username %}
<li><a href="/user/list">usersList</a></li>
{% endif %}
```
### 视图保护

上面虽然实现了对于页面相关接口的控制显示，但是通过输入网址仍可以访问相关网页，这时候就需要**实现对于视图函数访问的控制**。

因为视图保护功能在很多视图函数中都会用到，所以编写装饰器函数来实现功能：
```Python
# libs.py
def login_required(func):
    @wraps(func)
    def decorate_nest(*args,**kwargs):
        # user为设置的session参数
        if not 'user' in session:
            return redirect(url_for("user_app.login"))
        else:
            return func(*args,**kwargs)
    return decorate_nest
```
## 其他

### 密码哈希化

对于密码的加密，在`models.py`中使用`werkzeug.security`中相关函数实现了密码的加密。

### 分页显示

对于内容过多的页面，使用分页显示是比较好的选择，在 `users.py`中使用 `paginate`实现了用户列表的分页显示。

### `ckeditor`

在文章书写和编辑中使用 `ckeditor`代替HTML原生的 `textarea`，格式见`user`相应的HTML文件。

# 需要继续学习的地方
 - [x] `libs.py`中装饰器使用的`wraps`
 - [ ] `upload.py`中的`ckeditor`上传文件出现`500`
 - [ ] **Javascript不太懂……**
 - [x] 文件传输中json和ajax相关