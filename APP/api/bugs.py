# -*- coding: utf-8 -*-

# @Time    : 2021/1/11 下午4:41
# @Author  : cyq
# @File    : bugs.py

from flask_restful import Api, Resource, reqparse
from APP import auth, db
from flask import g, jsonify
from Model.models import User, Bugs, Project, Product, ErrorType, Platform, Build
from APP.api import myBug
from .errors_or_auth import is_admin
from COMMENT.myRequestParser import MyRequestParser
from COMMENT.Log import get_log
from COMMENT.myResponse import myResponse

log = get_log(__file__)


class MyBugs(Resource):

    @auth.login_required
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=False, location='json')
        parse.add_argument("projectId", type=str, required=False, location='json')
        parse.add_argument("platformId", type=str, required=False, location='json')
        parse.add_argument("buildId", type=str, required=False, location='json')
        parse.add_argument("title", type=str, required=False, location='json')
        parse.add_argument("level", type=str, required=False, location='json')
        parse.add_argument("priority", type=str, required=False, location='json')
        parse.add_argument("assignedTo", type=str, required=False, location='json')
        parse.add_argument("mailTo", type=str, required=False, location='json')
        parse.add_argument("stepsBody", type=str, required=False, location='json')

        productId = parse.parse_args().get("productId")
        projectId = parse.parse_args().get("projectId")

        platformId = parse.parse_args().get("platformId")
        buildId = parse.parse_args().get("buildId")
        title = parse.parse_args().get("title")
        level = parse.parse_args().get("level")
        priority = parse.parse_args().get("priority")
        assignedTo = parse.parse_args().get("assignedTo")
        mailTo = parse.parse_args().get("mailTo")
        stepsBody = parse.parse_args().get("stepsBody")

        produ = Product.get(productId)
        proj = Project.get(projectId)
        Platform.get(platformId)
        Build.get(buildId)

        try:
            u = Bugs(title=title, creater=g.user.id, stepsBody=stepsBody, product=productId, build=buildId, level=level,
                     priority=priority, assignedTo=assignedTo, mailTo=mailTo, platform=platformId)
            u.save()
            return jsonify(myResponse(0, u.id, "ok"))
        except ErrorType as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    @is_admin
    def delete(self):
        pass


class BugLists(Resource):

    def get(self):
        pass


api_script = Api(myBug)
api_script.add_resource(MyBugs, "/bugOpt")