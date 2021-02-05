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
        parse.add_argument("projectId", type=str, required=False, location='json', help="err errorTypes")

        name = parse.parse_args().get("name")
        solutions = parse.parse_args().get("solutions")
        platforms = parse.parse_args().get("platforms")
        builds = parse.parse_args().get("builds")
        errorTypes = parse.parse_args().get("errorTypes")
        projectId = parse.parse_args().get(("projectId"))
        Project.get(projectId)
        Product.verify_name(name=name)
        pro = Product(name, projectId)
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
                ps = [Product.get(pid)]
            else:
                ps = Product.all()
            productInfo = [
                {"id": i.id,
                 "name": i.name,
                 "solutions": [{"solution_name": s.name, "id": s.id} for s in i.solutions_records],
                 "platforms": [{"platform_name": p.name, "id": p.id} for p in i.platforms_records],
                 "builds": [{"build_name": b.name, "id": b.id} for b in i.builds_records],
                 "errorTypes": [{"error_name": e.name, "id": e.id} for e in i.errorTypes_records],
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
        p = Product.get(ID)
        try:
            p.delete()
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
    def put(self):
        pid = request.args.get("productId")
        sid = request.args.get("solutionId")
        name = request.args.get("name")

        p = Product.get(pid)
        s = Solution.get(sid)

        if s not in p.solutions_records:
            return jsonify(myResponse(21, None, f"Product:{pid}  Not included {sid}"))

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))

        s.name = name
        s.save()

        return jsonify(0, s.id, "ok")

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("name", type=str, required=False, location='json', help="err solutions")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid)

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))

        try:
            s = Solution(name, pid)
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

        s = Solution.get(id)
        try:
            s.delete()
            return jsonify(myResponse(0, None, "ok"))
        except ErrorType as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class PlatformOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("productId")
        p = Product.get(pid)
        try:
            s = [{"platform_name": i.name, "id": i.id} for i in p.platforms_records]
            return jsonify(myResponse(0, s, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def put(self):
        pid = request.json.get("productId")
        pld = request.json.get("platformId")
        name = request.args.get("name")
        p = Product.get(pid)
        pl = Platform.get(pld)
        if pl not in p.platforms_records:
            return jsonify(myResponse(21, None, f"Product:{pid}  Not included {pld}"))
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        pl.name = name
        pl.save()
        return jsonify(0, pl.id, "ok")

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("name", type=str, required=False, location='json', help="err platform")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid)
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        try:
            p = Platform(name, pid)
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
        p = Platform.get(id)
        try:
            p.delete()
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
            b = [{"build_name": i.name, "id": i.id} for i in p.builds_records]
            return jsonify(myResponse(0, b, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def put(self):
        pid = request.json.get("productId")
        bid = request.json.get("buildId")
        name = request.json.get("name")
        p = Product.get(pid)
        b = Build.get(bid)
        if b not in p.builds_records:
            return jsonify(myResponse(21, None, f"Product:{pid}  Not included {bid}"))
            # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        b.name = name
        b.save()
        return jsonify(0, b.id, "ok")

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("name", type=str, required=False, location='json', help="err buildId")
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid)
        # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        try:
            b = Build(name, pid)
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
        b = Build.get(id)
        try:
            b.delete()
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
    def put(self):
        pid = request.args.get("productId")
        eid = request.args.get("errorId")
        name = request.args.get("name")
        p = Product.get(pid)
        e = ErrorType.get(eid)
        if e not in p.errorTypes_records:
            return jsonify(myResponse(21, None, f"Product:{pid}  Not included {eid}"))
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        e.name = name
        e.save()
        return jsonify(0, e.id, "ok")

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("productId", type=str, required=True, location="json", help="error productId")
        parse.add_argument("name", type=str, required=False, location='json', help="err errorType")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid)

        if name in [i.name for i in p.errorTypes_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        try:
            e = ErrorType(name, pid)
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
        e = ErrorType.get(id)
        try:
            e.delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))


class ProjectOpt(Resource):

    @auth.login_required
    def get(self):
        pid = request.args.get("projectId")
        p = Project.get(pid)
        try:
            e = [i.name for i in p.product]
            return jsonify(myResponse(0, e, "ok"))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(1, None, str(e)))

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("name", type=str, required=False, location='json', help="err errorType")
        name = parse.parse_args().get("name")
        Project.verify_name(name)
        try:
            p = Project(name)
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
