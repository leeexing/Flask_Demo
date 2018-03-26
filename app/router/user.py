# -*- coding: utf-8 -*-
"""users 视图"""

from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

mod_user = Blueprint('user', __name__,
                        template_folder='templates')

@mod_user.route('/user/home/')
def home():
    return render_template('base.html', name='User Home')

@mod_user.route('/user/setting/')
def setting():
    return render_template('base.html', name='User Setting')