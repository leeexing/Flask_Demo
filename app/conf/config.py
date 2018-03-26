# -*- coding: utf-8 -*-
# MySQL_URI = 'mysql://root@localhost:3306/flask?charset=utf8mb4'
MySQL_URI = 'mysql+mysqlconnector://root:123456@localhost/flask'    # 配置MySQL的URL格式为: mysql://username:password@hostname/database

# MONGO_URI = 'mongodb://10.13.62.202:27017/SITS'
MONGO_URI = 'mongodb://localhost:27017/myblog'
MONGO_DB_NAME = 'SITS'

Redis_URI = 'localhost'
Redis_Port = 6379


"""Tips
SQLAlchemy本身无法操作数据库，其必须以来pymsql等第三方插件，Dialect用于和数据API进行交流，根据配置文件的不同调用不同的数据库API，从而实现对数据库的操作.

MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
  
pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
  
MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

cx_Oracle
oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
"""