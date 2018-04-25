# -*- coding: utf-8 -*-
"""项目总体配置"""
from datetime import timedelta

class Config(object):
    """基本"""

    DEBUG = False
    SECRET_KEY = 'secret-key'   # change this !

    REDIS_URI = 'localhost'
    REDIS_PORT = 6379

class ProdConfig(Config):
    """生产"""

    MONGO_URI = 'mongodb://10.13.62.202:27017/NSTS'

class DevConfig(Config):
    """开发"""

    DEBUG = True
    SECRET_KEY = 'secret-key-leeing'

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否开启跟踪   # 每次请求结束都会自动提交事务
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost/flask'

    MONGO_URI = 'mongodb://localhost:27017/myblog'

    JWT_SECRET_KEY = 'super-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=24*60)
