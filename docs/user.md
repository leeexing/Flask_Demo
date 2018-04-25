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