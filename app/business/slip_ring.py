# -*- coding:utf-8 -*-
from app.common.fields import StatsFields
from flask_restful import marshal
from app.db import MONGO_DB as mongo
from app.util.response import ResponseHelper
from app.util.logger import create_logger
from datetime import datetime, timedelta

class SlipRingManager():
    """滑环业务类"""
    def __init__(self):
        self.logger = create_logger('SLIP_RING')

    def get_speed(self, eqp_id, args=None):
        """获取滑环转速"""
        try:
            start_time = args.start_time if args.start_time else datetime.now() - timedelta(days=1)
            end_time = args.end_time if args.end_time else datetime.now()
            result = list(mongo.db.slipring.find({
                'eqp_id': eqp_id,
                'name': 'SPEED',
                'clock': {'$gte': start_time, '$lte': end_time}},
                {'_id': 0, 'c_date': 0, 'eqp_id': 0, 'name': 0} # 将不需要的键排除掉
            ).sort({'clock': 1}))
            data = marshal(result, StatsFields.resource_fields) if result else None
            return ResponseHelper.return_true_data(data)
        except Exception as ex:
            self.logger.error('服务器错误！')
            return ResponseHelper.return_false_data(msg='Server Error', status=500)

    def get_motor_speed(self, eqp_id, args=None):
        """获取滑环电机转速"""
        try:
            start_time = args.start_time if args.start_time else datetime.now() - timedelta(days=1)
            end_time = args.end_time if args.end_time else datetime.now()
            result = list(mongo.db.slipring.find({
                'eqp_id': eqp_id,
                'name': 'MOTOR_SPEED',
                'clock': {'$gte': start_time, '$lte': end_time}},
                {'_id': 0, 'c_date': 0, 'eqp_id': 0, 'name': 0} # 将不需要的键排除掉
            ).sort({'clock': 1}))
            data = marshal(result, StatsFields.resource_fields) if result else None
            return ResponseHelper.return_true_data(data)
        except Exception as ex:
            self.logger.error('服务器错误！')
            return ResponseHelper.return_false_data(msg='Server Error', status=500)