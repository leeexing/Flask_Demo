# -*- coding: utf-8 -*-
import json


class ResponseHelper:
    @staticmethod
    def returnTrueJson(data, msg='success', status=200):
        return {
            "result": status,
            "data": data,
            "msg": msg
        }

    @staticmethod
    def returnFalseJson(data=None, msg="error", status=None):
        return {
            "result": status,
            "data": data,
            "msg": msg
        }
