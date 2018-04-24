# -*- coding:utf-8 -*-
"""用户模块类"""

from flask_restful import Resource
from flask_restful_swagger import swagger
from app.common.fields import (Register_Fileds, Register_Response_Fields, 
                                Login_Fields, Login_Response_Fields,
                                User_Query_Fields, Menu_Response_Fileds)
from app.business.user import UserManager

class Register(Resource):
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