# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午5:56
# @Author  : cyq
# @File    : myResponse.py

from .const import ResponseCode, ResponseError


def myResponse(code: ResponseCode, data, msg):
    if isinstance(msg,ResponseError):
        msg = msg.value
    return {"code": code.value, "data": data, "msg": msg}


def catchError(func):
    def wrapper(*args, **kwargs):
        try:
            u = func(*args, **kwargs)
            return u
        except Exception as e:
            result = repr(e)
            return myResponse(ResponseCode.ERROR, None, result)

    return wrapper
