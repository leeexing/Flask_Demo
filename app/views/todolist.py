# -*- coding: utf-8 -*-
"""
index 视图
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app.db import MONGO_DB as mongo

mod_todolist = Blueprint('todolist', __name__,
                                    template_folder='templates')

@mod_todolist.route('/')
def index():
    todos = mongo.db.todo.find({})
    print(todos)
    return render_template('todolist/todolist.html', name='Leeing', todos=todos)