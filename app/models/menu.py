# -*- coding:utf-8 -*-
from datetime import datetime
from app.db import MYSQL_DB as db
from app.models.user import EnumUserType, EnumSexType

class Menu(db.Model):
    """菜单"""
    __tablename__ = 'menu'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Name = db.Column(db.String(32), nullable=False)
    Pid = db.Column(db.Integer)
    Url = db.Column(db.String(50))
    Order = db.Column(db.Integer)
    CreateTime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    MenuConf = db.relationship('Menuconfig', backref='Menu', lazy='dynamic')

class Menuconfig(db.Model):
    """菜单配置"""
    __tablename__ = 'menuconfig'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    MenuID = db.Column(db.Integer, db.ForeignKey('menu.ID'), nullable=False)
    UserType = db.Column(db.Enum(EnumUserType))
    CreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Father(db.Model):
    """父亲表"""
    __tablename__ = 'father'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    position = db.Column(db.String(32))
    childrens = db.relationship('Children', backref='father', lazy='select')

class Children(db.Model):
    """孩子"""
    __tablename__ = 'children'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    sexType = db.Column(db.Enum(EnumSexType))
    fatherID = db.Column(db.Integer, db.ForeignKey('father.ID'))
