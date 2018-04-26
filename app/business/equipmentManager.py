# -*- coding: utf-8 -*-
from app.models.equipment import Equipment
from app.common.fields import EquipmentResourceFields
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
            return ResponseHelper.return_true_data(marshal(eqps, EquipmentResourceFields.resource_fields))
        except Exception as ex:
            return ResponseHelper.return_false_data(msg=str(ex), status=500)
