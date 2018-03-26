#-*- coding: utf-8 -*-
from flask import request
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

    @swagger.operation(
        notes = '添加用户数据',
        nickname = 'post',
        summary = '添加用户信息',
        responseClass = UserResourceFields,
        # required
        parameters = [{
            'name': 'body',
            'description': 'add user ...',
            'required': True,
            'allowMultiple': False,
            'dataType': UserResourceFields.__name__,
            'paramType': 'body'
        }],
        responseMessages = [
            {'code': 200, 'message': 'new user has saved'},
            {'code': 400, 'message': 'new user is required'},
            {'code': 500, 'message': 'JSON format not valid'}
        ]
    )
    def post(self):
        print('='*30)
        res = request.get_json()
        print(res)
        return self._users.insert_users(res)