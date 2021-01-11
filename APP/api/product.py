# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午7:51
# @Author  : cyq
# @File    : product.py

from flask_restful import Api, Resource, reqparse, request
from flask import jsonify
from APP.api import myBug
from COMMENT.myRequestParser import MyRequestParser
from COMMENT.Log import get_log
from COMMENT.myResponse import myResponse
from Model.models import Product, Solution, Build, Platform, ErrorType, Project
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
        parse.add_argument("projects", type=list, required=False, location='json', help="err errorTypes")

        name = parse.parse_args().get("name")
        solutions = parse.parse_args().get("solutions")
        platforms = parse.parse_args().get("platforms")
        builds = parse.parse_args().get("builds")
        errorTypes = parse.parse_args().get("errorTypes")
        projects = parse.parse_args().get(("projects"))

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
            if projects:
                for p in projects:
                    Project.verify_name(p)
                    Project(name=p, productId=pro.id).save()
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
                ps = [Product.get(pid)]
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

    @auth.login_required
    @is_admin
    def put(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productName", type=str, required=True, location="json", help="error name")
        parse.add_argument("productId", type=str, required=True, location="json", help="error name")

        name = parse.parse_args().get("productName")
        Id = parse.parse_args().get('productId')

        pro = Product.get(Id)
        Product.verify_name(name)
        if not pro:
            return jsonify(myResponse(1, None, f"{Id}  错误或不存在"))

        else:
            try:
                pro.name = name
                db.session.commit()
                return jsonify(myResponse(0, name, "ok"))
            except ErrorType as e:
                log.error(f"{__class__} {e}")
                db.session.rollback()
                return jsonify(myResponse(0, None, e))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")

        ID = parse.parse_args().get("productId")
        try:
            Product.get(ID).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            return jsonify(myResponse(1, None, str(e)))


class SolutionOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            s = [{"id": i.id, "name": i.name} for i in p.solutions_records]
            return jsonify(myResponse(0, s, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("solution", type=str, required=False, location='json', help="err solutions")

        pid = parse.parse_args().get("productId")
        sol = parse.parse_args().get("solution")

        p = Product.get(pid)

        try:
            s = [i.name for i in p.solutions_records]
            if sol in s:
                return jsonify(myResponse(1, None, f"{sol} 已存在"))
            else:
                s = Solution(sol, pid)
                s.save()
                return jsonify(myResponse(0, s.id, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=False, location='json', help="err solutions")
        id = parse.parse_args().get("id")
        try:
            Solution.get(id).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class PlatformOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            s = [i.name for i in p.platforms_records]
            return jsonify(myResponse(0, s, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("platform", type=str, required=False, location='json', help="err platform")

        pid = parse.parse_args().get("productId")
        pla = parse.parse_args().get("platform")

        p = Product.get(pid)

        try:
            pr = [i.name for i in p.platforms_records]
            if pla in pr:
                return jsonify(myResponse(1, None, f"{pla} 已存在"))
            else:
                p = Platform(pla, pid)
                p.save()
                return jsonify(myResponse(0, p.id, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=False, location='json', help="err id")
        id = parse.parse_args().get("id")
        try:
            Platform.get(id).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class BuildOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            b = [i.name for i in p.builds_records]
            return jsonify(myResponse(0, b, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("build", type=str, required=False, location='json', help="err buildId")

        pid = parse.parse_args().get("productId")
        bui = parse.parse_args().get("build")

        p = Product.get(pid)

        try:
            br = [i.name for i in p.builds_records]
            if bui in br:
                return jsonify(myResponse(1, None, f"{bui} 已存在"))
            else:
                b = Build(bui, pid)
                b.save()
                return jsonify(myResponse(0, b.id, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=False, location='json', help="err id")
        id = parse.parse_args().get("id")
        try:
            Build.get(id).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class ErrorTypeOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            e = [i.name for i in p.errorTypes_records]
            return jsonify(myResponse(0, e, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("errorType", type=str, required=False, location='json', help="err errorType")

        pid = parse.parse_args().get("productId")
        et = parse.parse_args().get("errorType")

        p = Product.get(pid)

        try:
            er = [i.name for i in p.errorTypes_records]
            if et in er:
                return jsonify(myResponse(1, None, f"{et} 已存在"))
            else:
                e = ErrorType(et, pid)
                e.save()
                return jsonify(myResponse(0, e.id, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=False, location='json', help="err id")
        id = parse.parse_args().get("id")
        try:
            ErrorType.get(id).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class ProjectOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            e = [i.name for i in p.projects_records]
            return jsonify(myResponse(0, e, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("name", type=str, required=False, location='json', help="err errorType")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid)
        Project.verify_name(name)
        try:
            names = [i.name for i in p.errorTypes_records]
            if name in names:
                return jsonify(myResponse(1, None, f"{name} 已存在"))
            else:
                p = Project(name, pid)
                p.save()
                return jsonify(myResponse(0, p.id, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=False, location='json', help="err id")
        id = parse.parse_args().get("id")
        try:
            Project.get(id).delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


api_script = Api(myBug)
api_script.add_resource(ProductOpt, '/productOpt')
api_script.add_resource(SolutionOpt, '/solutionOpt')
api_script.add_resource(BuildOpt, '/buildOpt')
api_script.add_resource(ErrorTypeOpt, '/errorTypeOpt')
api_script.add_resource(PlatformOpt, '/platformOpt')
api_script.add_resource(ProjectOpt, '/projectOpt')
