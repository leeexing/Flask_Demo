# -*- coding: utf-8 -*-
"""
users 视图
对于大量的views我倾向于使用flask的blueprint来实现对view的分类整理，将功能一致的view放在一个文件里面
"""

from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
def home():
    return render_template('user/user.html', name='User Home')

@user_bp.route('/user/setting/')
def setting():
    return render_template('user/user.html', name='User Setting')