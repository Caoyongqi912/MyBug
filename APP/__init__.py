# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午2:49
# @Author  : cyq
# @File    : __init__.py.py


from flask import Flask
from COMMENT.config import config


def create_app(config_name="default"):
    """
    :param config_name: appConfig
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app

