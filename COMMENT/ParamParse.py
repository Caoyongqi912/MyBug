# -*- coding: utf-8 -*-

# @Time    : 2021/2/7 上午10:47
# @Author  : cyq
# @File    : ParamParse.py

from flask import request
from flask_restful import abort
from COMMENT.myResponse import myResponse
from COMMENT.const import *


class MyParse:
    """
    模仿flask_restful reqparse 自定义校验参数

    """

    def __init__(self):
        self.location = "json"
        self.args = []
        self.body = {}

    def add(self, **kwargs):
        self.location = kwargs.get("location", "json")
        # 默认类型为字符
        if not kwargs.get("type"):
            kwargs.setdefault("type", str)
        # 默认非必传
        if not kwargs.get("required"):
            kwargs.setdefault("required", False)

        self.body = getattr(request, self.location, {})
        self.args.append(kwargs)

    def parse_args(self):
        """
        参数校验
        :return:
        """
        for kw in self.args:
            if kw['required'] is True:
                if not self.body.get(kw['name']) or self.body.get(kw['name']) == "":
                    abort(myResponse(TypeError, None, cantEmpty(kw['name'])))

                # 类型判读
                if not isinstance(self.body[kw['name']], kw['type']):
                    abort(myResponse(TypeError, None, errorType(kw['name'])))
                # choice 判断
                if kw.get('choices'):
                    if self.body[kw['name']] not in kw['choices']:
                        abort(myResponse(TypeError, None, errorValue(kw['name'])))
            else:
                if self.body.get(kw['name']):
                    # 类型判读
                    if not isinstance(self.body[kw['name']], kw['type']):
                        abort(myResponse(TypeError, None, f"{kw['name']}: error type"))
                    # choice 判断
                    if kw.get('choices'):
                        if self.body[kw['name']] not in kw['choices']:
                            abort(myResponse(TypeError, None, f"{kw['name']}: error value"))

                if kw.get("default") and self.body.get(kw['name']) is None:
                    self.body[kw['name']] = kw.get('default')

        return self.body



class Constant:
    JSON = "json"
    ARGS = "args"


class SearchParamsParse:
    from APP import create_app
    from sqlalchemy import create_engine

    condition = ["in", "not in", "=", ">", "<"]
    OR = "or "
    AND = "and "
    sql = f"select * from bugs where "
    eng = create_engine(create_app().config['SQLALCHEMY_DATABASE_URI'], echo=False)

    def __init__(self, body: list, opt: str):

        self.option = opt
        self.body = self._verify(body)
        self.param = None

    def _verify(self, body: list) -> list:
        for b in body:
            if not b.get("key") and not b.get("condition") and not b.get("val"):
                abort(myResponse(SQL_PARAM_ERROR, None, "invalid params"))
            if b.get("condition") not in self.condition:
                abort(myResponse(SQL_PARAM_ERROR, None, f"{b.get['condition']}  is  invalid "))

        return body

    def _paramParse(self):
        sql = ""

        if self.option == self.OR:
            for b in self.body:
                s = " ".join([b.get("key"), b.get("condition"), '"' + str(b.get('val')) + '"', self.OR])
                sql += s
        else:
            for b in self.body:
                s = " ".join([b.get("key"), b.get("condition"), '"' + str(b.get('val')) + '"', self.AND])
                sql += s
        return sql.strip("and ")

    def filter(self) -> list:
        sql = self.sql + self._paramParse()
        try:
            res = self.eng.execute(sql)
            return res.fetchall()
        except Exception as e:

            abort(myResponse(SQL_ERROR, None, SOME_ERROR_TRY_AGAIN))


if __name__ == '__main__':
    # a = [{'key': 'id', 'condition': '>', 'val': 1},
    #      {'key': 'level', 'condition': '=', 'val': 'p1'}]
    #
    # s = SearchParamsParse(a, "and")
    # s.filter()
    pass