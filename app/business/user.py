# -*- coding:utf-8 -*-
"""用户业务类"""

from flask import request
from flask_restful import marshal
from app.db import MYSQL_DB as db
from app.models.menu import Menu, Menuconfig
from app.models.user import User, EnumUserType
from app.util.response import ResponseHelper
from app.util.logger import create_logger
from app.util.image_storage import storage
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, jwt_optional, get_jwt_claims
import re

class UserObject:
    """用户对象"""

    def __init__(self, userid, username, usertype):
        self.userid = userid
        self.username = username
        self.usertype = usertype

class UserManager:
    """用户处理业务类"""

    def __init__(self):
        self.logger = create_logger('FLASK')

    @jwt_optional
    def user_register(self):
        """用户添加"""

        ret = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        if not ret['current_identity']:
            return ResponseHelper.return_false_data(msg='请登陆', status=200)
        user_id = ret.get('current_identity')[0]
        user_type = ret.get('current_type')
        if 1 == user_type:
            user_info = request.get_json()
            if not user_info:
                return ResponseHelper.return_false_data(msg='参数错误', status=200)
            user_name = user_info.get('user_name')
            password = user_info.get('password')
            name = user_info.get('name')
            # 验证完整性
            if not all([user_name, password, user_type]):
                return ResponseHelper.return_false_data(msg='账号密码不完整', status=200)
            if not re.match(r'[a-z, A-Z]*\d*$', user_name):
                return ResponseHelper.return_false_data(msg='账号格式不正确', status=200)
            try:
                user = User.query.filter_by(UserName=user_name).first()
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            if user:
                return ResponseHelper.return_false_data(msg='用户名已注册', status=200)
            # 添加用户
            user = User(UserName=user_name, Name=name,
                        CreatorId=user_id, UserType=EnumUserType(int(user_type)))
            user.password = password
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                db.session.rollback()
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            user_data = {
                'username': user.UserName,
                'name': user.Name
            }
            return ResponseHelper.return_true_data(data=user_data)
        else:
            return ResponseHelper.return_false_data(msg='权限不足', status=200)

    def user_login(self):
        """用户登陆"""

        user_info = request.get_json()
        if not user_info:
            return ResponseHelper.return_false_data(msg='参数错误', status=200)
        user_name = user_info.get('user_name')
        password = user_info.get('password')
        if not all([user_name, password]):
            return ResponseHelper.return_false_data(msg='账号密码不完整', status=200)
        try:
            user = User.query.filter_by(UserName=user_name).first()
        except Exception as e:
            self.logger.error('服务器错误：%s', str(e))
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        if not user or not user.check_password(password):
            return ResponseHelper.return_false_data(msg='用户名或密码错误', status=200)
        