# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午7:51
# @Author  : cyq
# @File    : product.py

from flask_restful import Api, Resource, reqparse, request
from flask import jsonify
from APP.api import myBug
from COMMENT.myRequestParser import MyRequestParser
from COMMENT.Log import get_log
from COMMENT.MyResponse import myResponse
from Model.models import Product, Solution, Build, Platform, ErrorType
from .errors_or_auth import is_admin
from APP import auth, db

log = get_log(__file__)


class ProductOpt(Resource):

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("name", type=str, required=True, location="json", help="error name")
        parse.add_argument("solutions", type=list, required=False, location='json', help="err solutions")
        parse.add_argument("platforms", type=list, required=False, location='json', help="err platforms")
        parse.add_argument("builds", type=list, required=False, location='json', help="err builds")
        parse.add_argument("errorTypes", type=list, required=False, location='json', help="err errorTypes")

        name = parse.parse_args().get("name")
        solutions = parse.parse_args().get("solutions")
        platforms = parse.parse_args().get("platforms")
        builds = parse.parse_args().get("builds")
        errorTypes = parse.parse_args().get("errorTypes")

        Product.verify_name(name=name)
        pro = Product(name)
        pro.save()
        try:
            if solutions:
                for s in solutions:
                    Solution.verify_name(s)
                    Solution(name=s, productId=pro.id).save()
            if platforms:
                for p in platforms:
                    Platform.verify_name(p)
                    Platform(name=p, productId=pro.id).save()
            if builds:
                for b in builds:
                    Build.verify_name(b)
                    Build(name=b, productId=pro.id).save()
            if errorTypes:
                for e in errorTypes:
                    ErrorType.verify_name(e)
                    ErrorType(name=e, productId=pro.id).save()

            return jsonify(myResponse(0, None, "ok"))

        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(0, None, e))

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        try:
            if pid:
                ps = Product.query.get(pid)
                if not ps:
                    return jsonify(myResponse(1, None, f"{pid}  错误或不存在"))
                ps = [ps]
            else:
                ps = Product.all()
            productInfo = [
                {"id": i.id,
                 "name": i.name,
                 "solutions": [s.name for s in i.solutions_records],
                 "platforms": [p.name for p in i.platforms_records],
                 "builds": [b.name for b in i.builds_records],
                 "errorTypes": [e.name for e in i.errorTypes_records],
                 }
                for i in ps]
            return jsonify(myResponse(0, productInfo, "ok"))

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"错误:{str(e)}"))


api_script = Api(myBug)
api_script.add_resource(ProductOpt, '/productOpt')
