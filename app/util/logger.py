# -*- coding:utf-8 -*-
"""日志模块"""
import logging
import os

def create_logger(name):
    """创建特定的日志输出"""
    logger = logging.getLogger(name) # 获取logger实例，如果参数为空则返回 root logger
    logger.setLevel(logging.INFO) # 指定日志的最低输出级别，默认为WARN级别
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # 指定logger输出格式

    if not logger.handlers:
        # 控制台日志
        chandler = logging.StreamHandler()
        chandler.setFormatter(formatter)
        # chandler.formatter = formatter # 也可以直接这样指定输出格式
        chandler.setLevel(logging.INFO)
        logger.addHandler(chandler)

        # 文件日志
        fhandler = logging.FileHandler(os.path.join('./', 'log.log'), encoding='utf-8', delay='true')
        fhandler.setLevel(logging.ERROR)
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler) # 为文件 logger 添加的日志处理器

        # logger.removeHandler(fhandler) # 移除一些日志处理器
    return logger
