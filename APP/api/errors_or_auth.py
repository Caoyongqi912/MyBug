# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:50
# @Author  : cyq
# @File    : errors_or_auth.py

from functools import wraps
from flask import g, jsonify, make_response, request
from Model.models import User
from . import myBug
from .. import auth
from COMMENT.Log import get_log

log = get_log(__name__)


@myBug.after_request
def after_request(response):
    return response


@myBug.before_request
def logWrite():
    log.info(
        f"[ request url = {request.url} | request Host = {request.host} | request Method = {request.method}")


@myBug.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 404, "data": "", 'msg': '没权限啊铁汁'}), 200


@myBug.app_errorhandler(500)
def host_err(e):
    return jsonify({"code": 500, "data": "", 'msg': '没权限啊铁汁'}), 200


@myBug.app_errorhandler(403)
def host_err(e):
    return jsonify({"code": 403, "data": "", 'msg': '没权限啊铁汁'}), 200


@auth.error_handler
def unauthorized():
    return jsonify({"code": 401, "data": "", 'msg': '没权限啊铁汁'}), 200


@auth.verify_password
def verify_password_or_token(username_or_token, password):
    user = User.verify_token(token=username_or_token)
    if not user:
        user = User.query.filter(User.account == username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def is_admin(func):
    """判断登录用户是否是admin"""

    @wraps(func)
    def wrap_func(*args, **kwargs):
        try:
            if not g.user.is_superuser():
                return make_response(
                    jsonify({"code": 1, "data":"",'meg': '没权限啊铁汁'}), 200)
            return func(*args, **kwargs)
        except KeyError:
            return make_response(
                jsonify({"code": 1,"data":"", 'meg': '没权限啊铁汁'}), 403)

    return wrap_func
