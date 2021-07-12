# -*- coding: utf-8 -*-

# @Time    : 2021/3/26 下午5:01
# @Author  : cyq
# @File    : search.py

from flask_restful import Api, Resource

from APP import auth
from APP.api import myBug
from flask import jsonify
from COMMENT.const import *
from COMMENT.ParamParse import MyParse


class Search(Resource):

    @auth.login_required
    def post(self):
        """
        全局搜索
        :return:
        """
        parse = MyParse()

        parse.add(name="opt", choices=range(1, 6), type=int, required=True)
        parse.add(name="searchID", type=int, required=True)

        opt = parse.parse_args().get("opt")
        id = parse.parse_args().get("searchID")
        return jsonify(myResponse(ResponseCode.SUCCESS, SearchOpt[opt].get(id,"searchID",obj=False), ResponseError.OK))


api_script = Api(myBug)
api_script.add_resource(Search, '/search')
