# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_cors import CORS
from app.conf.config import DevConfig
from flask_jwt_extended import JWTManager
from app.db import MYSQL_DB as db, MONGO_DB as mongo
import app.views as views


def create_app():
    """创建App"""
    app = Flask(__name__)
    app.config.from_object(DevConfig) # 初始化配置项

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'msg': 'The token has expired'
        }), 401

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return user.usertype

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        data = [user.userid, user.username]
        return data

    db.init_app(app)    # 初始化MYSQL数据库
    mongo.init_app(app) # 初始化MONGODB数据库
    CORS(app)           # 跨域支持
    api_bp = Blueprint('api', __name__)
    api = swagger.docs(Api(api_bp), apiVersion='0.1', resourcePath='/',
                       description='EMDP_API', api_spec_url='/swagger') # swagger支持
    bind_resources(api) # restful 的逻辑
    app.register_blueprint(api_bp, url_prefix='/api')   # 蓝图注册

    bind_views(app)
    return app

def bind_views(app):
    """注册客户端视图，蓝图绑定"""
    # @app.before_request
    # def before_request(Exception=None):
    #     print('=*'*10 + ' this runs before request ' + '*='*10)

    # @app.teardown_request
    # def teardown_request(Exception=None):
    #     print('+='*10 + ' this runs after request ' + '+='*10)

    app.register_blueprint(views.home_bp, url_prefix='/home')
    app.register_blueprint(views.user_bp)
    app.register_blueprint(views.todolist_bp, url_prefix='/todolist')

def bind_resources(api):
    """绑定对应资源"""

    from app.resources.equipment import Equipments
    api.add_resource(Equipments, '/equipments', endpoint='equipments')

    # TODO_List
    from app.resources.todolist import Todo, Todos, TodoStat
    api.add_resource(Todos, '/todos', endpoint='todos')
    api.add_resource(Todo, '/todo', endpoint='todo')
    api.add_resource(TodoStat, '/todo/<int:status>', endpoint='todostat')

    # 用户注册
    from app.resources.user import Register, Login, UserQuery, UsersQuery, SetUserAvatar
    api.add_resource(Register, '/user/register')
    api.add_resource(Login, '/user/login')
    api.add_resource(UsersQuery, '/users')
    api.add_resource(UserQuery, '/users/<string:id>')
    api.add_resource(SetUserAvatar, '/user/setavatar')
