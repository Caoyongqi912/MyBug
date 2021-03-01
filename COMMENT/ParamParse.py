# -*- coding: utf-8 -*-

# @Time    : 2021/2/7 上午10:47
# @Author  : cyq
# @File    : ParamParse.py

from flask import request
from flask_restful import abort
from COMMENT.myResponse import myResponse


class MyParse:
    """
    模仿flask_restful reqparse 自定义校验参数

    """

    def __init__(self):
        self.args = []
        self.body = {}

    def add(self, **kwargs):
        self.location = kwargs.get("location")
        if not self.location:
            kwargs.setdefault("location", "json")
            self.location = "json"

        t = kwargs.get("req_type")
        if not t:
            kwargs.setdefault("req_type", str)

        required = kwargs.get("required")
        if not required:
            kwargs.setdefault("required", True)


        self.args.append(kwargs)
        self.body = getattr(request, self.location, {})

    def parse_args(self):
        for arg in self.args:
            if arg.get('choices'):
                if self.body[arg['name']] not in arg['choices']:
                    abort(400, **myResponse(44, None, f"{arg['name']}:  error value"))

            if arg['required'] is True:
                if arg['name'] not in self.body.keys():
                    abort(400, **myResponse(44, None, f"{arg['name']}:  cannot be empty"))

                if not isinstance(self.body[arg['name']], arg['req_type']):
                    abort(400, **myResponse(44, None, f"{arg['name']}:  error type"))

        return self.body

    def test(self):
        method = getattr(request, "method", {})
        data = getattr(request, "data", {})
        args = getattr(request, "args", {})
        value = getattr(request, "values", {})
        form = getattr(request, "form", {})
        json = getattr(request, "json", {})

        print("method", method)
        print(f"data  {data}")
        print(f"args  {args}")
        print(f"value {value}")
        print(f"form  {form}")
        print(f"json  {json}")


if __name__ == '__main__':
    a = {}

    print(a.get("f"))