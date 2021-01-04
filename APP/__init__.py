# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午2:49
# @Author  : cyq
# @File    : __init__.py.py


from flask import Flask
from COMMENT.config import config
from COMMENT.AlchemyOpt import MyBugBaseQuery
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

db = SQLAlchemy(model_class=MyBugBaseQuery)
auth = HTTPBasicAuth()
catch = Cache()


def create_app(config_name="default"):
    """
    :param config_name: appConfig
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    catch.init_app(app)
    # 设置跨域
    CORS(app, supperts_credentals=True)

    return app

