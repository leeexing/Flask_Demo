# -*- coding: utf-8 -*-
"""socketIO文件"""
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from app.conf.config import MySQL_URI, MONGO_DB_NAME, MONGO_URI
from app.db import MYSQL_DB as db, MONGO_DB as mongo
from threading import Lock

app = Flask('FLASK_WS')
app.config['SQLALCHEMY_DATABASE_URI'] = MySQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MONGO_DBNAME'] = MONGO_DB_NAME
app.config['MONGO_URL'] = MONGO_URI
db.init_app(app)
mongo.init_app(app)
CORS(app) # 支持跨域
socketio = SocketIO(app)

THREAD_LOCK = Lock()
TEST_THREAD = None

def emit_data_to_client():
    count = 1
    while True:
        count += 1
        socketio.emit('my response', {'data': count}, namespace='/test')
        socketio.sleep(1)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})
    with THREAD_LOCK:
        global TEST_THREAD
        if not TEST_THREAD:
            TEST_THREAD = socketio.start_background_task(emit_data_to_client)

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data'], 'count': 2})
