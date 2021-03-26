# -*- coding: utf-8 -*-

# @Time    : 2021/3/26 上午10:26
# @Author  : cyq
# @File    : savefile.py


import os


def getFilePath(file: str) -> str:
    path = os.path.dirname(os.path.abspath(__file__))
    return path + f"/{file}"
