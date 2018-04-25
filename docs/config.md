# 配置项

## 配置项一些参数的说明

```py
SQLAlchemy本身无法操作数据库，其必须以来pymsql等第三方插件，
Dialect用于和数据API进行交流，根据配置文件的不同调用不同的数据库API，从而实现对数据库的操作.

MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

cx_Oracle
oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
```