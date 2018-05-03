# -*- coding:utf-8 -*-
"""用户模块类"""

from flask_restful import Resource
from flask_restful_swagger import swagger
from app.common.fields import (Register_Fileds, Register_Response_Fields, 
                               Login_Fields, Login_Response_Fields,
                               User_Query_Fields, Menu_Response_Fileds)
from app.business.user import UserManager, Family

class Register(Resource):
    """注册"""

    def __init__(self):
        self.user_manager = UserManager()

    @swagger.operation()
    def post(self):
        result = self.user_manager.register()
        return result

class UserRegister(Resource):
    """注册"""

    def __init__(self):
        self.user_manager = UserManager()

    @swagger.operation()
    def post(self):
        result = self.user_manager.user_register()
        return result

class Login(Resource):
    """注册"""

    def __init__(self):
        self.user_manager = UserManager()

    def post(self):
        result = self.user_manager.user_login()
        return result

class UserQuery(Resource):
    """查询用户"""

    def __init__(self):
        self.user_manager = UserManager()

    def get(self, id):
        result = self.user_manager.user_query(id)
        return result

class UsersQuery(Resource):
    """查询用户列表"""

    def __init__(self):
        self.user_manager = UserManager()

    def get(self):
        result = self.user_manager.users_query()
        return result

class SetUserAvatar(Resource):
    """上传用户头像"""

    def __init__(self):
        self.user_manager = UserManager()

    def post(self):
        result = self.user_manager.set_user_avatar()
        return result

class FatherAdd(Resource):
    """添加父亲角色"""

    def __init__(self):
        self.family = Family()

    def post(self):
        result = self.family.add_father()
        return result

class ChildAdd(Resource):
    """添加孩子角色"""

    def __init__(self):
        self.family = Family()

    def post(self):
        result = self.family.add_child()
        return result

class QueryChildren(Resource):
    """获取父亲的孩子"""

    def __init__(self):
        self.family = Family()

    def get(self, fathername):
        result = self.family.get_children_by_father_name(fathername)
        return result

class QueryFather(Resource):
    """获取孩子的父亲"""

    def __init__(self):
        self.family = Family()

    def get(self, childname):
        result = self.family.get_father(childname)
        return result