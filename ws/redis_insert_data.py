# -*- coding:utf-8 -*-
"""往redis数据库中插入数据"""
from pymongo import MongoClient
from redis import StrictRedis
from datetime import datetime, timedelta
import string
from time import sleep
from random import randint, sample, random
import json

STRING_FORSELECT = string.ascii_letters + '0123456789' + '加几个中国汉字也挺好'

mongo = MongoClient('localhost')
db = mongo.myblog
R = StrictRedis(host='localhost', port=6379)

# data = db.todo.find({})
# print(list(data))
ret = R.hget('leeing:hash', 'obj')
print(ret)

def save_mongo():
    """保存数据到mongodb、redis"""
    for i in range(500):
        time = datetime.now() - timedelta(hours=randint(0, 23), minutes=randint(0, 60), seconds=randint(0, 60), weeks=randint(0,3))
        obj = {
            'title': ''.join(sample(STRING_FORSELECT, randint(5, 10))),
            'status': True if random() > 0.5 else False,
            'create_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(obj)
        R.hset('leeing:slip', 'todo', json.dumps(obj))
        db.todo.save(obj)
        sleep(1.5)

save_mongo()