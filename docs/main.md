# 主文件

> 关于配置项

## flask_pymongo

flask_pymongo
在设置配置项的时候，原先是这么写的
结果：报错
`pymongo.errors.InvalidName: database names cannot contain the character '.'`

```py
# main.py
from app.db import MYSQL_DB as db, MONGO_DB as mongo

mongo.init_app(app) # 初始化MONGODB数据库
```

```py
# app/conf/config.py

class DevConfig(Config):

    MONGO_URI = 'mongodb://localhost:27017'
    # MONGO_URI = 'mongodb://root:123456@10.13.62.202:27017/SITS'
    MONGO_DBNAME = 'myblog'
```

正解：
MONGO_URI = **'mongodb://localhost:27017/myblog'**
单单只在后面添加有个 `/` 也不行。

其实正确的写法是两种

```py
# 方法一
app = Flask(__name__)
app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_DBNAME='flask',
    MONGO_USERNAME='bjhee',
    MONGO_PASSWORD='111111'
)
方法一，指定了MongoDB的服务器地址、端口、数据库名称、用户名和密码

# 方法二
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
    MONGO_USERNAME='bjhee',
    MONGO_PASSWORD='111111'
)
方法二是方法一的简化

# 拓展
# 可以初始化两个以上的 Flask-PyMongoDB 实例。分别基于不同的配置项
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
    MONGO_USERNAME='bjhee',
    MONGO_PASSWORD='111111',
    MONGO_TEST_URI='mongodb://localhost:27017/test'
)

mongo = PyMongo(app)
mongo_test = PyMongo(app, config_prefix='MONGO_TEST')

当调用初始化方法”PyMongo()”时，传入”config_prefix”参数，该PyMongo实例就会使用以”MONGO_TEST”为前缀的配置项，而不是默认的”MONGO”前缀，比如上例中的”MONGO_TEST_URI”。
```

题外：
`mongo.db.users`用来获取名为`users`结合对象

NOTES: 从拓展可以看出，两种配置方法的不一样。
总结：
MONGO_TEST_URI：需要后面带数据库名
MONGO_DBNAME：简单就是数据库名，需要配合 `MONGO_HOST`、`MONGO_PORT` 一起使用

参考：
[Flask-PyMongo](https://www.cnblogs.com/Erick-L/p/7047064.html)

## Blueprint

> 蓝图

蓝图的概念，可以分别定义模块的视图、模板、视图等等