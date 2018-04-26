# Flask_pyMongo

> 具体如何使用查询

## 添加

```py
mongo.db.user.insert_one({'username': 'leeing', 'password': '123456'})  # 创建一条

mondo.db.user.insert_many([{'username': 'lee-'+ i} for i in range(3)]) # 创建多条
```

## 查询

```py
mongo.db.user.find({}) # 所有

mongo.db.user.find({'username': 'lee-1'})

mongo.db.user.find({'age': {'$lt': 24}}) # 大于条件

mongo.db.user.find().sort('name')

from flask_pymongo import DESCENDING
mongo.db.user.find().sort('age', DESCENDING)

mongo.db.user.find().limit(5).skip(2)

mongo.db.user.find().distinct('age')
```

## 更新

```py
mongo.db.user.update_one({'username': 'lee-1'}, {'$set': {'age': 20}})
mongo.db.user.update_one({'username': 'lee-1'}, {'$inc': {'age': 2}}) # 年龄增加两岁

user = {'username': 'lee-11', 'age': 23}
mongo.db.user.replace_one({'username':'lee-1'}, user)
```

## 删除

```py
mongo.db.user.delete_one({'username': 'lee-1'})

mongo.db.user.delete_many({'age': {'$gt': 30}})
```

## 参考

(flask 扩展 flask_pymongo[https://www.cnblogs.com/Erick-L/p/7047064.html]