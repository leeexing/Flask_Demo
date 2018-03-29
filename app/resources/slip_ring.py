# -*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Resource
from flask_restful_swagger import swagger
from app.common.fields import StatsFields
from app.business.slip_ring import SlipRingManager

class SlipSpeed(Resource):
    """获取滑环速度"""
    def __init__(self):
        self.slip_ring = SlipRingManager()

    @swagger.operation(
        notes='',
        nickname='get',
        summary='',
        parameters=[
            
        ]
    )
