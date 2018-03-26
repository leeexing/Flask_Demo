# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.main import create_app
from app.db import MYSQL_DB as db

app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)   # 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

manager.add_command('runserver', Server(host='0.0.0.0', port=5002, use_debugger=True))
manager.add_command('db',MigrateCommand)    # manager是Flask-Script的实例，这条语句在flask-script中添加一个db命令

if __name__ == '__main__':
    manager.run()
