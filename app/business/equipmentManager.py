# -*- coding: utf-8 -*-
from app.models.equipment import Equipment, User
from app.common.fields import EquipmentResourceFields, UserResourceFields
from app.util.response import ResponseHelper
from flask_restful import marshal   # marshal 对象序列化和反序列化


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
        """获取用户"""
        try:
            print(7777)
            print(User)
            items = User.query.with_entities(User.username, User.age, User.password).all()
            print(9999)
            rets = []
            for item in items:
                rets.append({
                    'username': item.username,
                    'age': item.age,
                    'password': item.password
                })
            print('='*30)
            print(rets)
            print('='*30)
            return ResponseHelper.returnTrueJson(marshal(rets, UserResourceFields.resource_fileds))
        except Exception as ex:
            print(88888)
            return ResponseHelper.returnFalseJson(msg = str(ex), status = 500)

    def insert_users(self, data):
        """添加用户信息"""
        try:
            print(6666)
        except Exception as ex:
            return ResponseHelper.returnTrueJson(msg=str(ex))
