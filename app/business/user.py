# -*- coding:utf-8 -*-
"""用户业务类"""

from flask import request
from flask_restful import marshal
from app.db import MYSQL_DB as db
from app.models.menu import Menu, Menuconfig, Father, Children
from app.models.user import User, EnumUserType, EnumSexType
from app.util.response import ResponseHelper
from app.util.logger import create_logger
from app.util.image_storage import storage
from app.conf.instance import QINIU_DOMAIN_PREFIX
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

    def register(self):
        """用户注册【主动】"""

        user_info = request.get_json()
        if not user_info:
            return ResponseHelper.return_false_data(msg='参数错误', status=200)
        user_name = user_info.get('user_name')
        password = user_info.get('password')
        name = user_info.get("name")
        user_type = user_info.get("user_type")
        if not all([user_name, password]):
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
        user = User(UserName=user_name, Name=name, UserType=EnumUserType(int(user_type)))
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

    @jwt_optional
    def user_register(self):
        """用户添加【被动】"""

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
        user_type = user.UserType.value
        user_id = user.ID
        name = user.Name
        user_avatar = user.AvatarUrl
        user_obj = UserObject(userid=user_id, username=user_name, usertype=user_type)
        access_token = create_access_token(identity=user_obj)
        res_data = {
            'accessToken': access_token,
            'userName': user_name,
            'userID': user_id,
            'name': name,
            'userAvatar': user_avatar,
            'expiresIn': 24*60
        }
        return ResponseHelper.return_true_data(res_data)

    @jwt_optional
    def user_query(self, use_id):
        """用户查询"""

        cur = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        if not cur['current_identity']:
            return ResponseHelper.return_false_data(msg='请登录', status=200)
        user_type = cur.get('current_type')
        if 1 == user_type:
            try:
                user = User.query.filter_by(ID=int(use_id)).first()
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            if user:
                user_data = {
                    'id': user.ID,
                    'username': user.UserName,
                    'name': user.Name,
                    'usertype': user.UserType
                }
                return ResponseHelper.return_true_data(user_data)
        else:
            return ResponseHelper.return_false_data(msg='权限不足', status=200)

    @jwt_optional
    def users_query(self):
        """用户列表查询"""

        cur = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        if not cur['current_identity']:
            return ResponseHelper.return_false_data(msg='请登录', status=200)
        user_type = cur.get('current_type')
        if 1 == user_type:
            try:
                users = User.query.all()
                print(users)
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            if users:
                users_list = [dict(userid=user.ID, username=user.UserName,
                                   name=user.Name, usertype=user.UserType.value) for user in users]
                return ResponseHelper.return_true_data(users_list)
        else:
            return ResponseHelper.return_false_data(msg='权限不足', status=200)

    @jwt_optional
    def user_type_upd(self):
        """用户类型修改"""

        cur = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        if not cur['current_identity']:
            return ResponseHelper.return_false_data(msg='请登录', status=200)
        user_type = cur.get('current_type')
        if 1 == user_type:
            user_info = request.get_json()
            if not user_info:
                return ResponseHelper.return_false_data(msg='参数错误', status=200)
            user_id = user_info.get('user_id')
            user_type = user_info.get('user_type')
            if not all([user_id, user_type]):
                return ResponseHelper.return_false_data(msg='参数不完整', status=200)
            try:
                User.query.filter_by(ID=user_id).update({'UserType': EnumUserType(user_type)})
                db.session.commit()
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                db.session.rollback()
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            return ResponseHelper.return_true_data('用户类型修改成功')
        else:
            return ResponseHelper.return_false_data(msg='权限不足', status=200)

    @jwt_optional
    def set_user_avatar(self):
        """用户头像上传"""

        cur = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        print(request.files)
        if not cur['current_identity']:
            return ResponseHelper.return_false_data(msg='请登录', status=200)
        user_name = cur.get('current_identity')[1]
        avatar = request.files.get('avatar')
        print(avatar)
        if not avatar:
            return ResponseHelper.return_false_data(msg='图像未上传', status=200)
        avatar_data = avatar.read()
        try:
            image_name = storage(avatar_data)
        except Exception as e:
            self.logger.error('服务器错误：', str(e))
            return ResponseHelper.return_false_data(msg='七牛云图片上传失败', status=200)
        avatar_url = QINIU_DOMAIN_PREFIX + image_name
        try:
            User.query.filter_by(UserName=user_name).update({'AvatarUrl': avatar_url})
            db.session.commit()
        except Exception as e:
            self.logger.error('服务器错误：', str(e))
            db.session.rollback()
            return ResponseHelper.return_false_data(msg='用户头像保存失败', status=200)
        return ResponseHelper.return_true_data(avatar_url)

    @jwt_optional
    def user_menu(self):
        """用户菜单"""

        cur = {
            'current_identity': get_jwt_identity(),
            'current_type': get_jwt_claims()
        }
        if not cur['current_identity']:
            return ResponseHelper.return_false_data(msg='请登录', status=200)
        user_type = cur.get('current_type')
        if user_type:
            try:
                menus = Menuconfig.query.filter_by(UserType=EnumUserType(user_type)).all()
            except Exception as e:
                self.logger.error('服务器错误：', str(e))
                return ResponseHelper.return_false_data(msg='Server Error', status=500)
            if menus:
                menu_list = [dict(menuname=menu.Menu.Name, menuurl=menu.Menu.Url,
                                  menupid=menu.Menu.Pid) for menu in menus]
                return ResponseHelper.return_true_data(menu_list)
            else:
                return ResponseHelper.return_false_data(msg='请添加菜单', status=200)
        else:
            return ResponseHelper.return_false_data(msg='请添加角色', status=200)

########## Family ###########

class Family:
    """测试关系型数据库的深刻含义"""

    def __init__(self):
        self.logger = create_logger('Flask')

    def add_father(self):
        """添加父亲"""
        info = request.get_json()
        print('+='*20)
        print(info)
        father_name = info.get('name')
        father_position = info.get('position')
        try:
            father_db = Father.query.filter_by(name=father_name).first()
        except Exception as ex:
            print('Error happend %s'%str(ex))
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        if father_db:
            return ResponseHelper.return_false_data(msg='数据已存在', status=200)
        father = Father(name=father_name, position=father_position)
        try:
            db.session.add(father)
            db.session.commit()
        except Exception as ex:
            print('error happend %s'%str(ex))
            db.session.rollback()
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        father_data = {
            'name': father_name,
            'position': father_position
        }
        return ResponseHelper.return_true_data(father_data)


    def add_child(self):
        """添加孩子"""

        info = request.get_json()
        print('+-'*20)
        print(info)
        name = info.get('name')
        age = info.get('age')
        sex_type = info.get('sexType')
        father_name = info.get('fatherName')
        father = Father.query.filter_by(name=father_name).first()
        child = Children(name=name, age=age, sexType=EnumSexType(int(sex_type)), fatherID=father.ID)
        try:
            db.session.add(child)
            db.session.commit()
        except Exception as ex:
            print('Errro happen %s'%str(ex))
            db.session.rollback()
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        child_data = {
            'name': name,
            'age': age,
            'sex': child.sexType.name,
            'fatherID': father.ID
        }
        return ResponseHelper.return_true_data(child_data)

    def get_children_by_father_name(self, name):
        """查询父亲有几个孩子"""

        print('=+'*20)
        print(request.args)
        father_name = request.args.get('name')
        try:
            father = Father.query.filter_by(name=father_name).first()
            if not father:
                return ResponseHelper.return_false_data(msg='父亲用户名不存在', status=200)
            childrens = father.childrens2
        except Exception as ex:
            self.logger.error('服务器错误:%s', str(ex))
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        print(childrens)
        childrens_list = [dict(name=child.name, age=child.age,
                               sex=child.sexType.name) for child in childrens]
        get_data = {
            'fatherName': name,
            'childrens': childrens_list
        }
        return ResponseHelper.return_true_data(get_data)

    def get_father(self, name):
        """查询孩子的父亲是谁"""

        try:
            child = Children.query.filter_by(name=name).first()
            if not child:
                return ResponseHelper.return_false_data(msg='孩子名不存在', status=200)
            father = child.father
        except Exception as ex:
            print('Error happend %s'%str(ex))
            return ResponseHelper.return_false_data(msg='Server Error', status=500)
        print(father)
        data = {
            'childName': name,
            'fatherName': father.name
        }
        return ResponseHelper.return_true_data(data)
