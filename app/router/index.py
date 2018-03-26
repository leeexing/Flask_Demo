# -*- coding: utf-8 -*-
"""
index 视图
"""
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

mod_index = Blueprint('home', __name__,
                            template_folder='templates')

@mod_index.route('/')
def index():
    return render_template('base.html', name='Leeing')