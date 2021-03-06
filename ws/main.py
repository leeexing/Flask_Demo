# -*- coding: utf-8 -*-
"""socketIO文件"""
from flask import Flask, request
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS
from threading import Lock
from app.conf.config import DevConfig
from app.db import MYSQL_DB as db, MONGO_DB as mongo
from app.util.logger import create_logger

app = Flask('FLASK_WS')
app.config.from_object(DevConfig)

db.init_app(app)
mongo.init_app(app)
CORS(app) # 支持跨域
socketio = SocketIO(app)


###################### WS_TEST ############################

@socketio.on('connect', namespace='/test')
def connect():
    """test 连接"""
    from ws.ws_test import test_connect
    test_connect()

@socketio.on('disconnect', namespace='/test')
def disconnect():
    """test 断开连接"""
    from ws.ws_test import test_disconnect
    test_disconnect()

@socketio.on('test message', namespace='/test')
def test_message(msg):
    """test 发送消息"""
    emit('my response', {'data': msg['data']})


####################### SLIP_RING ##########################

@socketio.on('connect', namespace='/SLIP_RING')
def connect():
    """test 连接"""
    from ws.slip_ring import slipring_connect
    slipring_connect()

@socketio.on('disconnect', namespace='/SLIP_RING')
def disconnect():
    """test 断开连接"""
    from ws.slip_ring import slipring_disconnect
    slipring_disconnect()

@socketio.on('client_response', namespace='/SLIP_RING')
def test_message(msg):
    """test 发送消息"""
    emit('server_response', {'data': msg['data']})
