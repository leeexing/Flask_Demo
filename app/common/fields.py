# -*- coding: utf-8 -*-
from flask_restful import fields
from flask_restful_swagger import swagger

# ------------ equipment ------------

@swagger.model
class EquipmentResourceFields:
    resource_fields = {
        # 'result': fields.Integer,
        # 'data': fields.List(fields.Nested(equipment_fields)),
        # 'msg': fields.String
        'Latitude': fields.Float,
        'Longitude': fields.Float,
        'EQP_ID': fields.String,
        'Type': fields.String,
        'Location': fields.String
    }

@swagger.model
class UserResourceFields:
    resource_fields = {
        'username': fields.String,
        'password': fields.String
    }
    def __init__(self, arg1, arg2, arg3='123'):
        pass

class ClockItem(fields.Raw):
    def format(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

@swagger.model
class TodoResourceFileds:
    resource_fields = {
        'title': fields.String,
        'status': fields.Boolean,
        'create_time': ClockItem
    }

@swagger.model
class StatsFields:
    resource_fields = {
        'title': fields.String
    }