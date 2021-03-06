# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午7:51
# @Author  : cyq
# @File    : product.py
from flask import g
from flask_restful import Api, Resource
from flask import jsonify
from APP.api import myBug
from COMMENT.Log import get_log
from COMMENT.ParamParse import MyParse
from Model.models import *
from .errors_or_auth import is_admin
from APP import auth
from COMMENT.const import *


log = get_log(__file__)


class ProductOpt(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="name", required=True)
        parse.add(name="solutions", type=list)
        parse.add(name="platforms", type=list)
        parse.add(name="builds", type=list)
        parse.add(name="errorTypes", type=list)
        parse.add(name="projectId", type=int)
        parse.add(name='module', type=list)

        name = parse.parse_args().get("name")
        solutions = parse.parse_args().get("solutions")
        platforms = parse.parse_args().get("platforms")
        builds = parse.parse_args().get("builds")
        errorTypes = parse.parse_args().get("errorTypes")
        projectId = parse.parse_args().get(("projectId"))
        modules = parse.parse_args().get("module")
        Project.get(projectId, 'projectId')
        Product.verify_name(name)
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
                    Build(name=b, productId=pro.id, builder=g.user.name).save()
            if errorTypes:
                for e in errorTypes:
                    ErrorType.verify_name(e)
                    ErrorType(name=e, productId=pro.id).save()

            if modules:
                for m in modules:
                    Module.verify_name(m)
                    Module(name=m, productId=pro.id).save()

            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))

        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=False, location='args')
        pid = parse.parse_args().get("productId")
        try:
            if pid:
                ps = [Product.get(pid, "productId")]
            else:
                ps = Product.all()
            productInfo = [
                {"id": i.id,
                 "name": i.name,
                 "solutions": [{"solution_name": s.name, "id": s.id} for s in i.solutions_records],
                 "platforms": [{"platform_name": p.name, "id": p.id} for p in i.platforms_records],
                 "builds": [{"build_name": b.name, "id": b.id} for b in i.builds_records],
                 "errorTypes": [{"error_name": e.name, "id": e.id} for e in i.errorTypes_records],
                 "modules": [{'module_name': m.name, "id": m.id} for m in i.modules_records]
                 }
                for i in ps]
            return jsonify(myResponse(ResponseCode.SUCCESS, productInfo, ResponseError.OK))
        except Exception as e:
            log.exception(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:

        parse = MyParse()
        parse.add(name="productName", required=True)
        parse.add(name="productId", required=True)
        name = parse.parse_args().get("productName")
        Id = parse.parse_args().get('productId')

        pro = Product.get(Id, 'productId')
        Product.verify_name(name)
        if not pro:
            return jsonify(myResponse(ResponseCode.ERROR, None, cantEmpty(Id)))

        else:
            try:
                pro.name = name
                db.session.commit()
                return jsonify(myResponse(ResponseCode.SUCCESS, name, ResponseError.OK))
            except ErrorType as e:
                log.error(f"{__class__} {e}")
                db.session.rollback()
                return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True)
        ID = parse.parse_args().get("productId")
        p = Product.get(ID, 'productId')
        try:
            p.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class SolutionOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True, location='args')
        pid = parse.parse_args().get("productId")
        p = Product.get(pid, 'productId')

        try:
            s = [{"id": i.id, "name": i.name} for i in p.solutions_records]
            return jsonify(myResponse(ResponseCode.SUCCESS, s, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, location="args")
        parse.add(name="solutionId", req_type=int, location="args")
        parse.add(name="name", location="args")

        pid = parse.args.get("productId")
        sid = parse.args.get("solutionId")
        name = parse.args.get("name")

        p = Product.get(pid, "productId")
        s = Solution.get(sid, "solutionId")

        if s not in p.solutions_records:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, f"Product:{pid}  Not included {sid}"))

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, alreadyExists(name)))

        s.name = name
        s.save()

        return jsonify(ResponseCode.SUCCESS, s.id, ResponseError.OK)

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId")
        parse.add(name="name")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid, "productId")

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))

        try:
            s = Solution(name, pid)
            s.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, s.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="solutionId")
        id = parse.parse_args().get("solutionId")

        s = Solution.get(id, "solutionId")
        try:
            s.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except ErrorType as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class PlatformOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.args.get("productId")
        p = Product.get(pid, 'productId')
        try:
            s = [{"platform_name": i.name, "id": i.id} for i in p.platforms_records]
            return jsonify(myResponse(ResponseCode.SUCCESS, s, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="platformId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        pld = parse.parse_args().get("platformId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')
        pl = Platform.get(pld, 'platformId')
        if pl not in p.platforms_records:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, f"Product:{pid}  Not included {pld}"))
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        pl.name = name
        pl.save()
        return jsonify(myResponse(ResponseCode.SUCCESS, pl.id, ResponseError.ResponseError.OK))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True)
        parse.add(name="name", required=True)

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid, 'productId')
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        try:
            p = Platform(name, pid)
            p.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, p.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = MyParse()
        parse.add(name="platformId", required=True)
        id = parse.parse_args().get("platformId")
        p = Platform.get(id, 'platformId')
        try:
            p.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class BuildOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location="args", required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid, 'productId')
        try:
            b = [{"build_name": i.name, "id": i.id} for i in p.builds_records]
            return jsonify(myResponse(ResponseCode.SUCCESS, b, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="buildId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        bid = parse.parse_args().get("buildId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')
        b = Build.get(bid, "buildId")
        if b not in p.builds_records:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, f"Product:{pid}  Not included {bid}"))
            # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        b.name = name
        b.save()
        return jsonify(myResponse(ResponseCode.SUCCESS, b.id, ResponseError.ResponseError.OK))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", type=int, required=True)
        parse.add(name="name", required=True)
        parse.add(name="desc", type=str)
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        desc = parse.parse_args().get("desc")
        p = Product.get(pid, 'productId')
        # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        try:
            b = Build(name, pid, g.user.name, desc)
            b.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, b.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="buildId", type=int, required=True)
        id = parse.parse_args().get("buildId")
        b = Build.get(id, 'buildId')
        try:
            b.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class ErrorTypeOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid, 'productId')
        try:
            e = [i.name for i in p.errorTypes_records]
            return jsonify(myResponse(ResponseCode.SUCCESS, e, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="errorId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        eid = parse.parse_args().get("errorId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')
        e = ErrorType.get(eid, 'errorId')
        if e not in p.errorTypes_records:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, f"Product:{pid}  Not included {eid}"))
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        e.name = name
        e.save()
        return jsonify(myResponse(ResponseCode.SUCCESS, e.id, ResponseError.ResponseError.OK))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')

        if name in [i.name for i in p.errorTypes_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        try:
            e = ErrorType(name, pid)
            e.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, e.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="errorId", type=int, required=True)
        id = parse.parse_args().get("errorId")
        e = ErrorType.get(id, 'errorId')
        try:
            e.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class ModuleOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid, 'productId')
        try:
            e = [i.name for i in p.modules_records]
            return jsonify(myResponse(ResponseCode.SUCCESS, e, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="name", required=True)
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')

        if name in [i.name for i in p.modules_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        try:
            m = Module(name, pid)
            m.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, m.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="moduleId", type=int, required=True)

        e = Module.get(parse.parse_args().get("moduleId"), 'moduleId')
        try:
            e.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="moduleId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        mid = parse.parse_args().get("moduleId")
        name = parse.parse_args().get("name")
        p = Product.get(pid, 'productId')
        e = Module.get(mid, 'moduleId')
        if e not in p.modules_records:
            return jsonify(myResponse(ResponseCode.Error_Relation, None, f"Product:{pid}  Not included {mid}"))
        if name in [i.name for i in p.modules_records]:
            return jsonify(myResponse(ResponseCode.UNIQUE, None, alreadyExists(name)))
        e.name = name
        e.save()
        return jsonify(myResponse(ResponseCode.SUCCESS, e.id, ResponseError.ResponseError.OK))


class ProjectOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name='projectId', required=False, location="args")
        pid = parse.parse_args().get("projectId")
        try:
            if pid:
                p = [Project.get(pid, "projectId")]
            else:
                p = Project.all()
            info = [
                {"id": i.id, "name": i.name, "product": [j.name for j in i.product_records]}
                for i in p]
            return jsonify(myResponse(ResponseCode.SUCCESS, info, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="name", required=True)
        name = parse.parse_args().get("name")
        Project.verify_name(name)
        try:
            p = Project(name)
            p.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, p.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="projectId", type=int, required=True)
        id = parse.parse_args().get("projectId")
        try:
            Project.get(id, 'projectId').delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


api_script = Api(myBug)
api_script.add_resource(ProductOpt, '/productOpt')
api_script.add_resource(SolutionOpt, '/solutionOpt')
api_script.add_resource(BuildOpt, '/buildOpt')
api_script.add_resource(ErrorTypeOpt, '/errorTypeOpt')
api_script.add_resource(PlatformOpt, '/platformOpt')
api_script.add_resource(ModuleOpt, "/moduleOpt")
api_script.add_resource(ProjectOpt, '/projectOpt')
