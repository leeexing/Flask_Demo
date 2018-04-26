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

# ------------ users ------------

@swagger.model
class Register_Fileds:
    resource_fileds = {
        'user_name': fields.String,
        'password': fields.String,
        'name': fields.String,
        'user_type': fields.Integer,
    }

@swagger.model
class Register_Response_Fields:
    resource_fileds = {
        'username': fields.String,
        'name': fields.String
    }

@swagger.model
class Login_Fields:
    resource_fields = {
        'user_name': fields.String,
        'password': fields.String
    }

@swagger.model
class Login_Response_Fields:
    resource_fields = {
        'access_token': fields.String,
        'user_name': fields.String,
        'userID': fields.Integer,
        'name': fields.String,
        'user_avatar': fields.String,
        'expiresIn': fields.String
    }

@swagger.model
class User_Query_Fields:
    resource_fileds = {
        'UserName': fields.String,
        'Name': fields.String,
        'UserType': fields.Integer
    }

@swagger.model
class Menu_Response_Fileds:
    resource_fields = {
        'Name': fields.String,
        'Url': fields.String,
        'Pid': fields.Integer
    }
