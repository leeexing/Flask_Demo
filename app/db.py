# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flask?charset=utf8mb4'
MYSQL_DB = SQLAlchemy()
MONGO_DB = PyMongo()