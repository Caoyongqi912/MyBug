# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:46
# @Author  : cyq
# @File    : __init__.py.py

from flask import blueprints

myBug = blueprints.Blueprint("myBug", __name__, url_prefix="/api")

from . import users, product, bugs, search
