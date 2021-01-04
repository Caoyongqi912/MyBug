# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:31
# @Author  : cyq
# @File    : AlchemyOpt.py


from flask_restful import abort
from flask_sqlalchemy import BaseQuery
from .Log import get_log

log = get_log(__name__)

class MyBugBaseQuery(BaseQuery):

    def filter_by(self, **kwargs):
        """
        过滤软删除
        :param kwargs:
        :return:
        """

        kwargs.setdefault('status',1)
        return super().filter_by(**kwargs)

    def get_or_noFind(self, ident):
        rv = self.get(ident)
        if not rv:
            abort(dict(code=1,data="",msg="id错误或不存在"))
        elif rv.status == 0:
            abort(dict(code=1,data="",msg="id已删除"))
        return rv


