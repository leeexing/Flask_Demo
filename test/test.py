# -*- coding:utf-8 -*-
"""
测试文件
提供一些测试数据
"""
import app.util.connector import get_redis_connection
import json, re
from string import ascii_letters

STRING_SELECT = ascii_letters + '0123456789'

R = get_redis_connection()

def main():
    pass

if __name__ == '__main__':
    main()