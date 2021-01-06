# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午5:56
# @Author  : cyq
# @File    : myResponse.py


def myResponse(code, data, msg):
    return {"code": code, "data": data, "msg": msg}


def catchError(func):
    def wrapper(*args, **kwargs):
        try:
            u = func(*args, **kwargs)
            return u
        except Exception as e:
            result = repr(e)
            return myResponse(1, None, result)

    return wrapper
