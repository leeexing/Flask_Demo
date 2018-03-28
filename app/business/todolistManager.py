# -*- coding: utf-8 -*-
from app.common.fields import TodoResourceFileds
from app.util.response import ResponseHelper
from flask_restful import marshal   # marshal 对象序列化和反序列化
from app.db import MONGO_DB as mongo
from datetime import datetime


class TodolistManager():
    """待办事项业务类"""

    def get_todos(self, name=None):
        """获取所有待办事项"""
        try:
            results = None
            if not name:
                results = list(mongo.db.todo.find({}))
            # print(results)
            return ResponseHelper.returnTrueJson(marshal(results, TodoResourceFileds.resource_fields))
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg = str(ex), status = 500)

    def insert_todo(self, data):
        """添加待办事项"""
        try:
            if type(data) == dict:
                data['create_time'] = datetime.now()
                is_exist = mongo.db.todo.find_one({'title': data['title']})
                print(54654)
                print(data['title'])
                print(is_exist)
                if not is_exist:
                    mongo.db.todo.insert(data)
                else:
                    print('数据已经存在，不用添加')
                results = data
                results = marshal(results, TodoResourceFileds.resource_fields) if results else None
                return ResponseHelper.returnTrueJson(results)
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex))

    def put_todo(self, data):
        """修改待办事项"""
        try:
            results = None
            data = marshal(results, TodoResourceFileds.resource_fields) if results else None
            return ResponseHelper.returnTrueJson(results)
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex))

    def delete_todo(self, data):
        """删除待办事项"""
        try:
            results = None
            data = marshal(results, TodoResourceFileds.resource_fields) if results else None
            return ResponseHelper.returnTrueJson(results)
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex))

    def get_status_todo(self, status):
        """获取完成/未完成的待办事项"""
        try:
            status = True if status == '1' else False
            results = list(mongo.db.todo.find({'finished': status}))
            print(results)
            results = marshal(results, TodoResourceFileds.resource_fields) if results else None
            return ResponseHelper.returnTrueJson(results)
        except Exception as ex:
            return ResponseHelper.returnFalseJson(msg=str(ex))