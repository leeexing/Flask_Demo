# User 模块

## jwt 的使用

```py
@jwt.user_identity_loader
    def user_identity_lookup(user):
        data = [user.userid, user.username]
        return data
```

这段代码使用的时候，获取到的数据从哪里来的呢？
答案是这里，在 login 的时候添加

```py

```