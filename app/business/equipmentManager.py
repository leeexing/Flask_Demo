# -*- coding: utf-8 -*-
from app.models.equipment import Equipment, User
from app.common.fields import EquipmentResourceFields, UserResourceFields
from app.util.response import ResponseHelper
from flask_restful import marshal   # marshal 对象序列化和反序列化
from app.db import MONGO_DB as mongo


class EquipmentManager():
    """设备处理业务类"""

    def get_equipments(self):
        """查询设备"""
        try:
            #session = Session()
            items = Equipment.query.with_entities(Equipment.Latitude, Equipment.Location,
                                                  Equipment.Longitude, Equipment.Type,
                                                  Equipment.Type, Equipment.EQP_ID).all()
            eqps = []
            for item in items:
                eqps.append({
                    'EQP_ID': item.EQP_ID,
                    'Location':  item.Location,
                    'Longitude': item.Longitude,
                    'Latitude': item.Latitude,
                    'Type': item.Type
                })
            return ResponseHelper.returnTrueJson(marshal(eqps, EquipmentResourceFields.resource_fields))
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex), status=500)

class UserManager():
    """用户处理业务类"""

    def get_users(self):
        """获取所有用户"""
        try:
            results = list(mongo.db.users.find({}))
            print(results)
            return ResponseHelper.returnTrueJson(marshal(results, UserResourceFields.resource_fields))
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg = str(ex), status = 500)

    def get_user(self, user_name):
        """获取具体用户信息"""
        try:
            results = list(mongo.db.users.find({'username': user_name}))
            print(results)
            return ResponseHelper.returnTrueJson(marshal(results, UserResourceFields.resource_fields))
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg = str(ex), status = 500)

    def insert_users(self, data):
        """添加用户信息"""
        try:
            if type(data) == dict:
                print(data['username'])
                user_is_exist = mongo.db.users.find_one({'username': data['username']})
                print(user_is_exist)
                if not user_is_exist:
                    mongo.db.users.insert(data)
                else:
                    print('数据已经存在，不用添加')
            else:
                for new_user in data:
                    user_is_exist = mongo.db.users.find_one({'username': data['username']})
                    if user_is_exist:
                        continue
                    mongo.db.user.save(data)
            results = data
            results = marshal(results, UserResourceFields.resource_fields) if results else None
            return ResponseHelper.returnTrueJson(results)
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex))
