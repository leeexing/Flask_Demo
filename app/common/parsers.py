# *-* coding:utf-8 *-*
"""参数解析"""

from flask_restful import reqparse

USER_PARSER = reqparse.RequestParser()
USER_PARSER.add_argument('username', type=str, location='args')
# USER_PARSER.add_argument('username', type=dict, location=['args', 'json']) #可以接收复合型的json参数


TODO_PARSER = reqparse.RequestParser()
TODO_PARSER.add_argument('title', type=str, location='args')