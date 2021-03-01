# -*- coding: utf-8 -*-

# @Time    : 2021/1/11 下午4:41
# @Author  : cyq
# @File    : bugs.py

from flask_restful import Api, Resource, reqparse
from APP import auth
from flask import g, jsonify
from Model.models import User, Bugs, Project, Product, ErrorType, Platform, Build
from APP.api import myBug
from .errors_or_auth import is_admin
from COMMENT.Log import get_log
from COMMENT.myResponse import myResponse
from COMMENT.ParamParse import MyParse

log = get_log(__file__)


class MyBugs(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        """
        增加一个bug信息
        :return: jsonify
        """
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=False)
        parse.add(name="projectId", req_type=int, required=False)
        parse.add(name="platformId", req_type=int, required=False)
        parse.add(name="buildId", req_type=int, required=False)
        parse.add(name="errorTypeId", req_type=int, required=False)
        parse.add(name="title")
        parse.add(name="level", choices=['p1', 'p2', 'p3', 'p4'], required=False)
        parse.add(name="priority", choices=['p1', 'p2', 'p3', 'p4'], required=False)
        parse.add(name="assignedTo", req_type=int)
        parse.add(name="mailTo", req_type=int, required=False)
        parse.add(name="stepsBody")

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

        project = Project.get(projectId)
        product = Product.get(productId)

        User.get(assignedTo)
        User.get(mailTo)

        if product not in project.product_records:
            return jsonify(myResponse(21, None, f"Project： Not included productId {productId}"))
        if int(platformId) not in [i.id for i in product.platforms_records]:
            return jsonify(myResponse(21, None, f"Product： Not included platformId {platformId}"))

        if int(buildId) not in [i.id for i in product.builds_records]:
            return jsonify(myResponse(21, None, f"Product： Not included buildId {buildId}"))

        try:
            u = Bugs(title=title, creater=g.user.id, stepsBody=stepsBody, product=productId, build=buildId)
            u.priority = priority
            u.level = level

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

    @auth.login_required
    def get(self):
        projects = Project.query.all()
        print(projects)



api_script = Api(myBug)
api_script.add_resource(MyBugs, "/bugOpt")
api_script.add_resource(BugLists, "/getBugs")
