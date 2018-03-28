# -*- coding: utf-8 -*-
"""
index 视图
"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

mod_index = Blueprint('home', __name__,
                            template_folder='templates')

@mod_index.route('/')
def index():
    return render_template('base.html', name='Leeing')

@mod_index.route('/ws')
def ws():
    return render_template('home/websocket.html', name='Socket')

@mod_index.route('/about')
def about():
    abort(404)

@mod_index.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')