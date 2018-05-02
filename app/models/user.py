# -*- coding:utf-8 -*-
from enum import Enum
from datetime import datetime
from app.db import MYSQL_DB as db
from werkzeug.security import generate_password_hash, check_password_hash

class EnumUserType(Enum):
    Admin = 1
    Common = 2

class EnumSexType(Enum):
    Man = 1
    Woman = 2

class User(db.Model):
    """用户"""
    __tablename__ = 'user'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    UserName = db.Column(db.String(32), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Name = db.Column(db.String(32))
    UserType = db.Column(db.Enum(EnumUserType))
    CreatorId = db.Column(db.String(128))
    AvatarUrl = db.Column(db.String(128))
    CreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        """获取密码"""
        raise AttributeError("不可直接访问")

    @password.setter
    def password(self, passwd):
        """设置密码，之前先哈希加密处理"""
        self.Password = generate_password_hash(passwd)

    def check_password(self, passwd):
        """检测密码是否正确，和原有密码进行哈希对比"""
        return check_password_hash(self.Password, passwd)