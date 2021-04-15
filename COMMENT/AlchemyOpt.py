# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:31
# @Author  : cyq
# @File    : AlchemyOpt.py


from flask_restful import abort
from flask_sqlalchemy import BaseQuery
from .Log import get_log
from .myResponse import myResponse

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

    def get_or_NoFound(self, ident, name):
        rv = self.get(ident)
        if not rv:
            abort(400, **myResponse(1, None, f"{name}: {ident} non-existent "))
        elif rv.status == 0:
            abort(400, **myResponse(1, None, f"{name}: {ident} Deleted"))
        return rv





