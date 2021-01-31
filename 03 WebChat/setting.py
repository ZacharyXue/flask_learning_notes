class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True  
    SQLALCHEMY_DATABASE_URI = "sqlite:///my.db" 
    SECRET_KEY = '123456'  # 不知道这里为什么必须大写，小写的时候就会报错

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

config = {
    'development': DevelopmentConfig,
    'production':ProductionConfig
}