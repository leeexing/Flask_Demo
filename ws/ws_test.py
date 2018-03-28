# -*- coding:utf-8 -*-
"""socket test"""

from threading import Lock
from flask import request
from flask_socketio import disconnect, join_room, leave_room, rooms, emit
from app.util.logger import create_logger
from app.util.connector import get_redis_connection
from ws.main import socketio

TEST_ROOM = {}
THREAD_LOCK = Lock()
TEST_THREAD = None
LOGGER = create_logger('WS_TEST')

R= get_redis_connection()


def emit_data_to_client():
    count = 1
    while True:
        count += 1
        socketio.emit('my response', {'data': count}, namespace='/test')
        socketio.sleep(1)

def test_connect():
    """test 测试连接socket"""
    LOGGER.info('%s connected in WS_TEST' % request.sid) # 前端页面发起请求的唯一id | 全局请求上下文( request context global)通过增加sid来支持为链接设置独一无二的session id。这个值在第一个用户进入房间是被使用。
    print(request.args)
    client_name = request.args.get('client_name', None)
    if not client_name:
        disconnect()
    join_room(client_name, namespace='/test')
    if client_name not in TEST_ROOM.keys():
        TEST_ROOM[client_name] = []
    TEST_ROOM[client_name].append(request.sid)
    print(TEST_ROOM)
    print('当前进入房间的是：', rooms(namespace='/test'))
    LOGGER.info('*'*15 + 'WS_TEST_ENTER_ROOM' + '*'*15)

    emit('my response', {'data': 'Connected', 'count': request.sid})
    with THREAD_LOCK:
        global TEST_THREAD
        if not TEST_THREAD:
            print(TEST_THREAD)
            TEST_THREAD = socketio.start_background_task(emit_data_to_client)

def test_message(message):
    emit('my response', {'data': message['data'], 'count': 2})

def test_disconnect():
    LOGGER.info(' {} disconnect from test ws !'.format(request.sid))
    print('当前想要离开房间的是：', rooms(namespace='/test'))
    for key in TEST_ROOM:
        if request.sid in TEST_ROOM[key]:
            TEST_ROOM[key].remove(request.sid)
            if not TEST_ROOM[key]: # TEST_ROOM[key] 为空的时候
                TEST_ROOM.pop(key, None)
            break
    for room in rooms(namespace='/test'):
        print('离开房间的到底是谁？' + room)
        leave_room(room, namespace='/test')
    LOGGER.info('+'*15 + 'WS_TEST_LEAVE_ROOM' + '+'*15)
    LOGGER.info(TEST_ROOM)
    print(rooms(namespace='/test'))
    disconnect()