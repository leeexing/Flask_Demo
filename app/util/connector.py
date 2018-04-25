# -*- coding:utf-8 -*-
"""数据库连接器"""
from redis import StrictRedis
from pymongo import MongoClient
from app.conf.config import Redis_Port, Redis_URI, DevConfig

def get_mongo_connection():
    """Mongodb连接器"""
    return MongoClient(host=DevConfig.MONGO_URI)

def get_redis_connection():
    """Redis连接器"""
    return StrictRedis(host=Redis_URI, port=Redis_Port, charset='utf-8', decode_responses=True)