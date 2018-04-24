# pylint

代码检测

## 使用

生成默认配置文件

```py
pylint --persistent=n --generate-rcfile > pylint.conf
```

check单个文件

```py
pylint --rcfile=pylint.conf manage.py
```

check整个工程

目前看只能一个module一个module的pylint，但是如果在工程根目录下添加init.py文件，即把工程当做一个python包的话，可以对整个工程进行pylint

```py
pylint api(api为包名称)
```

Tips: 重命名pylint.conf为.pylintrc，即不需要每次执行都带上--rcfile参数了