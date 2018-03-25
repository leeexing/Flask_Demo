#-*- coding: utf-8 -*-
from flask_restful import Resource
from flask_restful_swagger import swagger
from app.common.fields import EquipmentResourceFields, UserResourceFields
from app.business.equipmentManager import EquipmentManager, UserManager


class Equipments(Resource):
    def __init__(self):
        self._equipmentManager = EquipmentManager()

    @swagger.operation(
        notes='查询设备元数据',
        nickname='get',
        summary='查询设备元数据',
        responseClass=EquipmentResourceFields
    )
    def get(self):
        return self._equipmentManager.get_equipments()

class Users(Resource):
    def __init__(self):
        self._users = UserManager()

    @swagger.operation(
        notes = '获取用户数据',
        nickname = 'get',
        summary = '查询用户信息',
        responseClass = UserResourceFields
    )
    def get(self):
        return self._users.get_users()