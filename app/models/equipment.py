"""
mysql 数据库查询的时候需要建立 model
mongo 数据库查询的时候，不需要建立 model， 可以直接写语句进行数据库操作
"""
from datetime import datetime
from app.db import MYSQL_DB as db

#Base = declarative_base()  # 创建对象的基类


class Equipment(db.Model):
    """设备信息"""
    __tablename__ = 'equipment'

    # 表的结构
    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    EQP_ID = db.Column(db.String(45), nullable=False)
    Location = db.Column(db.String(45))
    Longitude = db.Column(db.Numeric(10, 6))
    Latitude = db.Column(db.Numeric(10, 6))
    Type = db.Column(db.String(45))
    IP = db.Column(db.String(45))
    Status = db.Column(db.Integer, nullable=False, default=1)
    CreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ModifyTime = db.Column(db.DateTime)


class User(db.Model):
    """用户信息"""
    __tablename__ = 'user'

    # 表的结构
    ID = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    username = db.Column(db.String(64), unique = True, index = True)
    # age = db.Column(db.Integer)
    password = db.Column(db.String(45))

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)
