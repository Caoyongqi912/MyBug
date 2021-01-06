# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:31
# @Author  : cyq
# @File    : AlchemyOpt.py


from flask_restful import abort
from flask_sqlalchemy import BaseQuery
from .Log import get_log
from .MyResponse import myResponse

log = get_log(__name__)



class MyBugBaseQuery(BaseQuery):

    def filter_by(self, **kwargs):
        """
        过滤软删除
        :param kwargs:
        :return:
        """

        kwargs.setdefault('status', 1)
        return super().filter_by(**kwargs)

    def get_or_NoFound(self, ident):
        rv = self.get(ident)
        if not rv:
            abort(400,description="err")
        elif rv.status == 0:
            handelAbort("id已删除")
        return rv

def handelAbort(msg):
    abort(dict(code=1, data="", msg=msg))

