# -*- coding: utf-8 -*-
"""输出类"""

class ResponseHelper:
    """输出帮助类"""
    @staticmethod
    def return_true_data(data, msg='success', status=200, **kwargs):
        """返回正确结果"""
        return {
            "result": status,
            "data": data,
            "msg": msg,
            **kwargs
        }

    @staticmethod
    def return_false_data(data=None, msg="error", status=None, **kwargs):
        """返回错误结果"""
        return {
            "result": status,
            "data": data,
            "msg": msg,
            **kwargs
        }
