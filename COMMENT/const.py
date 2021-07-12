# -*- coding: utf-8 -*-

# @Time    : 2021/3/10 上午9:51
# @Author  : cyq
# @File    : const.py
from Model.models import *

from enum import Enum


class ResponseCode(Enum):
    SUCCESS = 0
    ERROR = 1
    Error_Relation = 21
    UNIQUE = 31
    TypeError = 44
    SQL_ERROR = 93
    SQL_PARAM_ERROR = 99


class ResponseError(Enum):
    OK = "OK"
    ERROR_ACCOUNT = "ERROR ACCOUNT"
    SOME_ERROR_TRY_AGAIN = "SOME ERROR TRY AGAIN"
    NO_FIlE = "NO FIlE"
    INVALID_PARAMS = "INVALID PARAMS"


def alreadyExists(name):
    return f"name:{name} already exists "


def cantEmpty(name: str) -> str:
    return f"{name} cant not be empty or '' "


def errorType(name: str) -> str:
    return f"{name} INVALID TYPE"


def errorValue(name: str) -> str:
    return f"{name} INVALID VALUE "


SearchOpt = {
    1: Bugs,
    2: Product,
    3: Product,
    4: User,
    5: Build
}
