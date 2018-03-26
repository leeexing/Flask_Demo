# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_cors import CORS
from app.resources.equipment import Equipments, Users
from app.conf.config import MySQL_URI, MONGO_URI, MONGO_DB_NAME
from app.db import MYSQL_DB as db, MONGO_DB as mongo
from app.router.user import mod_user
from app.router.index import mod_index


def create_app():
    """创建App"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = MySQL_URI       # 定义URI        # 程序使用的数据库URL必须保存到SQLALCHEMY_DATABASE_URI变量
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 是否开启跟踪   # 每次请求结束都会自动提交事务
    app.config['MONGO_DBNAME'] = MONGO_DB_NAME
    app.config['MONGO_URI'] = MONGO_URI

    db.init_app(app)    # 初始化MYSQL数据库
    mongo.init_app(app) # 初始化MONGODB数据库
    CORS(app)  # 跨域支持
    api_bp = Blueprint('api', __name__)
    api = swagger.docs(Api(api_bp), apiVersion='0.1', resourcePath='/', description='EMDP_API', api_spec_url='/swagger') # swagger支持
    bind_resources(api)
    app.register_blueprint(api_bp, url_prefix='/page')
    # 注册视图
    app.register_blueprint(mod_user)
    app.register_blueprint(mod_index)
    return app

def bind_resources(api):
    """绑定对应资源"""
    api.add_resource(Equipments, '/equipments',endpoint='equipments')
    api.add_resource(Users, '/users', endpoint = 'users')