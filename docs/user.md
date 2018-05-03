# User 模块

## jwt 的使用

> jwt: json-web-token

概念：

1. use `create_access_token()` to make new access JWTs. 
  The create_access_token() function is used to actually generate the token, and you can return it to the caller however you choose.
2. the `jwt_required()` decorator to protect endpoints
3. and `get_jwt_identity()` function to get the identity of a JWT in a protected endpoint.
4. the `jwt_optional()` decorator will allow the endpoint to be accessed regardless of if a JWT is sent in with the request. to use one endpoint for both protected and unprotected data
5. You may want to **store additional information** in the access token which you could later access in the protected views。This can be done with the `user_claims_loader()` decorator, and the data can be accessed later in a protected endpoint with the `get_jwt_claims()` function.

简而言之：

* create_access_token：根据传入的参数，产生一个 token，可以通过 get_jwt_identity 获取之前传入数据
* jwt_required：保护（视图函数）端点必须通过 jwt 验证 -- 有一个正确的 token
* jwt_optional：比较自由，可以没有 jwt 验证这一步，必要的时候也可以通过 get_jwt_identity 获取到相应的 token 进行验证。If no JWT is sent in with the request，get_jwt_identity() will return None
* user_claims_loader() 装饰的视图函数中的参数，就是 `create_access_token(identity)` 里面的 **identity** （数据）

具体：

```py

@jwt.user_claims_loader
    def add_claims_to_access_token(user): 
        return user.usertype

@jwt.user_identity_loader
    def user_identity_lookup(user):
        data = [user.userid, user.username]
        return data
```

这段代码使用的时候，获取到的数据从哪里来的呢？
答案是这里，在 login 的时候添加

```py
# business/user.py
from flask_jwt_extended import create_access_token

  user_info = request.get_json()
  user_name = user_info.get('user_name')  # post请求传过来的数据
  password = user_info.get('password')

  user = User.query.filter_by(UserName=user_name).first() # 获取数据库里面的数据

  user_type = user.UserType.value
  user_id = user.ID
  name = user.Name
  user_avatar = user.AvatarUrl
  user_obj = UserObject(userid=user_id, username=user_name, usertype=user_type)
  # 这一段内容对应了上面的获取
  access_token = create_access_token(identity=user_obj)
```

那么，这些数据在什么时候，什么地方，怎么使用的呢？
答案就是在 需要去验证身份（`抬头处使用 🌈@jwt_optional🌈装饰器`）的接口的地方（视图函数），函数的开头做判断

```py
# business/register.py
from flask_jwt_extended import get_jwt_identity, jwt_optional, get_jwt_claims

@jwt_optional
def user_register(self):
    ret = {
        'current_identity': get_jwt_identity(),
        'current_type': get_jwt_claims()
    }
    if not ret['current_identity']:
        return ResponseHelper.return_false_data(msg='请登陆', status=200)
```

## SQLAlchemy

> 重点理解 relationship

```py demo
作者：知乎用户
链接：https://www.zhihu.com/question/38456789/answer/295687669
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    articles = relationship('Article')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class Article(Base):

    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)
```

每篇文章有一个外键指向 users 表中的主键 id， 而在 User 中使用 SQLAlchemy 提供的 relationship 描述 关系。而用户与文章的之间的这个关系是双向的，所以我们看到上面的两张表中都定义了 relationship。

SQLAlchemy 提供了 backref 让我们可以只需要定义一个关系：`articles = relationship('Article', backref='author')`
添加了这个就可以不用再在 Article 中定义 relationship 了！

__划重点__
这样既可以通过 Author实例.articles 获取到改作者的所有文章。也可以通过 Article实例.author 获取到改文章作者的具体信息。这里就是**backref**的功劳

```py 怎么使用
author = Author.query.filter_by(username='xxx').first()
author_articles = author.artcles
articles = [dict(title=aticle.title, content=article.content) for article in author_articles]


article = Article.query.filter_by(title='yyy').first()
article_author = article.author
# 这里就可以获取到作者的密码和邮箱等其他信息了
```

【参考】
[如何理解 SQLAlchemy中的relationship和backref](https://www.zhihu.com/question/38456789)