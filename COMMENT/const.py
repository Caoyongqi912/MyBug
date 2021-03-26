# -*- coding: utf-8 -*-

# @Time    : 2021/3/10 上午9:51
# @Author  : cyq
# @File    : const.py


SUCCESS = 0
ERROR = 1
Error_Relation = 21
UNIQUE = 31
TypeError = 44
SQL_ERROR = 93
SQL_PARAM_ERROR = 99

OK = "ok"
ERROR_ACCOUNT = 'err account'
SOME_ERROR_TRY_AGAIN = "some error try again"
NO_FIlE = "no file upload"



def cantEmpty(name:str) -> str:
    return f"{name} cant not be empty or '' "


def errorType(name:str) -> str:
    return f"{name} error type"


def errorValue(name:str) -> str:
    return f"{name} error value "