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

主要注意几个重要的API

1. Blueprint('', __name__, template_folder='', static_folder='', url_prefix='/')
2. .register_blueprint(api[, view], url_prefix='')

```py demo
# /app/music.py
from flask import Blueprint    #不用多说
 
musics=Blueprint('misics',__name__)       #创建一个blueprint对象。第一个参数可看做该blueprint对象的姓名
                                          #在一个app里，姓名不能与其余的Blueprint对象姓名重复
                                          #第二个参数__name__用作初始化
 
@musics.route("/music")                   #将蓝图对象当做‘app’那样使用
def music():
    return '这里是一首音乐~'

# /app/movie.py

from flask import Blueprint    #不用多说
 
movies=Blueprint('movies',__name__)
@movies.route("/movie")
def movie():
    return '这里是一部好片~'

# /app/main.py
from flask import Flask    # 不用多说
from blueprints import musics,movies    #导入blueprints目录下musics.py与movies.py模块,
 
app=Flask(__name__)    #创建 Flask()对象： app
 
@app.route('/')  #使用了蓝图，app.route() 这种模式就仍可以使用，注意路由重复的问题
def hello_world():
    return 'hello my world !'
 
app.register_blueprint(musics.musics)     # 将musics模块里的蓝图对象musics注册到app
app.register_blueprint(movies.movies)     # 将movies模块里的蓝图对象movies注册到app
 
if __name__=='__main__':
    app.run(debug=True)
```

蓝图既可以注册视图，也可以注册api。就看怎么安排了

`NOTES`：
注意和 `restful` 的区别

## RESTFUL

> api restful

掌握两个 API 的使用方法

1. Api(app)
2. add_resource()

```py demo
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
```

## request.args

获取路由问号（？）后面的参数

NOTE：
路由传参，字段里面不能夹带参数

```js wrong

http://localhost:5002/api/children/leeing?name='leeing'
```

```js right
http://localhost:5002/api/children/leeing?name=leeing
```

虽然通过 request.args.get('name') 也能拿到对应的字段值，但是通过数据库查询的时候，这就不是我们期待的那个值了

```py
father_name = request.args.get('name')
try:
    father = Father.query.filter_by(name=father_name).first()
    if not father:
        return ResponseHelper.return_false_data(msg='父亲用户名不存在', status=200)
    childrens = father.childrens2
except Exception as ex:
    self.logger.error('服务器错误:%s', str(ex))
    return ResponseHelper.return_false_data(msg='Server Error', status=500)
```

这里获取不到相应的数据