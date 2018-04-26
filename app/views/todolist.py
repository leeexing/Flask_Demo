# -*- coding: utf-8 -*-
"""
TODO_LIST 视图
"""
from flask import Blueprint, render_template
from app.db import MONGO_DB as mongo

todolist_bp = Blueprint('todolist', __name__)

@todolist_bp.route('/')
def index():
    """todo首页"""
    todos = mongo.db.todo.find().limit(10)
    print(todos)
    return render_template('todolist/todolist.html', name='Leeing', todos=todos)
