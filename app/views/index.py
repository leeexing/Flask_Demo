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

@mod_index.route('/socket')
def socket():
    return render_template('home/websocket.html', name='Socket')

@mod_index.route('/slip')
def slip_ring():
    return render_template('slipRing/slipRing.html', name='Socket')

@mod_index.route('/about')
def about():
    abort(404)

# errorhandler对该blueprint有效，但是需要注意的是404是不会被路又道blueprint的，出非404是在blueprint的view函数里面的abort的。建议使用 app_errorhandler
# @mod_index.errorhandler(404)  
@mod_index.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')