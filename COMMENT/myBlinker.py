# -*- coding: utf-8 -*-

# @Time    : 2021/1/6 下午4:05
# @Author  : cyq
# @File    : myBlinker.py

from datetime import datetime
from blinker import Namespace
from flask import request
from .Log import get_log

log = get_log(__file__)
# Namespace的作用:为了防止多人开发的时候，信号名字冲突的问题
mySignal = Namespace()
login_signal = mySignal.signal("login")


# 监听信号:监听信号使用singel对象的connect方法，在这个方法中需要传递一个函数，用来接收以后监听到这个信号该做的事情。示例代码如下:
def login_log(sender, username):
    now = datetime.now()
    ip = request.remote_addr
    info = "用户名: {},登录时间: {},ip地址: {}\n".format(username, now, ip)
    log.info(f"{login_log.__name__}  " + info)


login_signal.connect(login_log)
