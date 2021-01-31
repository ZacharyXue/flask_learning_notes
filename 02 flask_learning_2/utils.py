from app import db
from models import User

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