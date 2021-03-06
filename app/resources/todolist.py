#-*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from flask_restful_swagger import swagger
from app.common.fields import StatsFields, TodoResourceFileds
from app.business.todolistManager import TodolistManager
from app.common.parsers import TODO_PARSER


class Todos(Resource):
    def __init__(self):
        self._todos = TodolistManager()

    @swagger.operation(
        notes='获取所有待办事项',
        tags='Todo',
        nickname='get',
        summary='查询全部待办事项',
        responseClass=TodoResourceFileds
    )
    def get(self):
        return self._todos.get_todos()

class Todo(Resource):
    def __init__(self):
        self._todos = TodolistManager()

    @swagger.operation(
        notes='获取具体待办事项',
        nickname='get',
        summary='获取具体待办事项',
        responseClass=TodoResourceFileds,
        parameters=[
            {'name':'title', 'dataType': 'string', 'paramType': 'query'}
        ]
    )
    def get(self):
        print(TODO_PARSER.parse_args())
        title = TODO_PARSER.parse_args().get('title')
        return self._todos.get_status_todo(title)

    @swagger.operation(
        notes='添加待办事项',
        nickname='post',
        summary='添加待办事项',
        responseClass=TodoResourceFileds,
        parameters=[{
            'name': 'body',
            'description': 'add todo ...',
            'required': True,
            'allowMultiple': False,
            'dataType': TodoResourceFileds.__name__,
            'paramType': 'body'
        }],
        responseMessages=[
            {'code': 200, 'message': 'new user has saved'},
            {'code': 400, 'message': 'new user is required'},
            {'code': 500, 'message': 'JSON format not valid'}
        ]
    )
    def post(self):
        print('='*15 + '传递参数' + '='*15)
        print(request.form)
        title = request.form.get('title', None)
        return self._todos.insert_todo(title)

    @swagger.operation(
        notes='更新待办事项',
        nickname='put',
        summary='更新待办事项',
        responseClass=TodoResourceFileds
    )
    def put(self):
        data = request.get_json()
        return self._todos.put_todo(data)

    @swagger.operation(
        notes='删除待办事项',
        nickname='delete',
        summary='删除不需要的任务',
        responseClass=StatsFields
    )
    def delete(self):
        title = request.form.get('title', None)
        print(request.form)
        return self._todos.delete_todo(title)

class TodoStat(Resource):

    def __init__(self):
        self._todos = TodolistManager()

    @swagger.operation(
        notes='获取待办事项的状态',
        nickname='get',
        summary='获取待办事项的状态',
        responseClass=TodoResourceFileds
    )
    def get(self, status):
        return self._todos.get_status_todo(status)