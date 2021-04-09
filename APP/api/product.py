# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午7:51
# @Author  : cyq
# @File    : product.py
from flask import g
from flask_restful import Api, Resource
from flask import jsonify
from APP.api import myBug
from COMMENT.ParamParse import MyParse
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

        Project.get(projectId)
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
                    Build(name=b, productId=pro.id).save()
            if errorTypes:
                for e in errorTypes:
                    ErrorType.verify_name(e)
                    ErrorType(name=e, productId=pro.id).save()

            if modules:
                for m in modules:
                    Module.verify_name(m)
                    Module(name=m, productId=pro.id).save()

            return jsonify(myResponse(SUCCESS, None, OK))

        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=False, location='args')
        pid = parse.parse_args().get("productId")
        try:
            if pid:
                ps = Product.query.get(pid)
                if not ps:
                    return jsonify(myResponse(ERROR, None, f"{pid}  错误或不存在"))
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
                 "modules": [{'module_name': m.name, "id": m.id} for m in i.modules_records]
                 }
                for i in ps]
            return jsonify(myResponse(SUCCESS, productInfo, OK))

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=ERROR, data="", err=f"错误:{str(e)}"))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:

        parse = MyParse()
        parse.add(name="productName", required=True)
        parse.add(name="productId", required=True)
        name = parse.parse_args().get("productName")
        Id = parse.parse_args().get('productId')

        pro = Product.get(Id)
        Product.verify_name(name)
        if not pro:
            return jsonify(myResponse(ERROR, None, f"{Id}  错误或不存在"))

        else:
            try:
                pro.name = name
                db.session.commit()
                return jsonify(myResponse(SUCCESS, name, OK))
            except ErrorType as e:
                log.error(f"{__class__} {e}")
                db.session.rollback()
                return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True)
        ID = parse.parse_args().get("productId")
        p = Product.get(ID)
        try:
            p.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


class SolutionOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True, location='args')
        pid = parse.parse_args().get("productId")
        p = Product.get(pid)

        try:
            s = [{"id": i.id, "name": i.name} for i in p.solutions_records]
            return jsonify(myResponse(SUCCESS, s, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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

        p = Product.get(pid)
        s = Solution.get(sid)

        if s not in p.solutions_records:
            return jsonify(myResponse(Error_Relation, None, f"Product:{pid}  Not included {sid}"))

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(Error_Relation, None, f"name:{name} already exists "))

        s.name = name
        s.save()

        return jsonify(SUCCESS, s.id, OK)

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId")
        parse.add(name="name")

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid)

        # 验证同一 product name唯一
        if name in [i.name for i in p.solutions_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))

        try:
            s = Solution(name, pid)
            s.save()
            return jsonify(myResponse(SUCCESS, s.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="id")
        id = parse.parse_args().get("id")

        s = Solution.get(id)
        try:
            s.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except ErrorType as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


class PlatformOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.args.get("productId")
        p = Product.get(pid)
        try:
            s = [{"platform_name": i.name, "id": i.id} for i in p.platforms_records]
            return jsonify(myResponse(SUCCESS, s, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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
        p = Product.get(pid)
        pl = Platform.get(pld)
        if pl not in p.platforms_records:
            return jsonify(myResponse(Error_Relation, None, f"Product:{pid}  Not included {pld}"))
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        pl.name = name
        pl.save()
        return jsonify(SUCCESS, pl.id, OK)

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", required=True)
        parse.add(name="name", required=True)

        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")

        p = Product.get(pid)
        # 验证同一 product name唯一
        if name in [i.name for i in p.platforms_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        try:
            p = Platform(name, pid)
            p.save()
            return jsonify(myResponse(SUCCESS, p.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = MyParse()
        parse.add(name="id", required=True)
        id = parse.parse_args().get("id")
        p = Platform.get(id)
        try:
            p.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


class BuildOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location="args", required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid)
        try:
            b = [{"build_name": i.name, "id": i.id} for i in p.builds_records]
            return jsonify(myResponse(SUCCESS, b, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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
        p = Product.get(pid)
        b = Build.get(bid)
        if b not in p.builds_records:
            return jsonify(myResponse(Error_Relation, None, f"Product:{pid}  Not included {bid}"))
            # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        b.name = name
        b.save()
        return jsonify(SUCCESS, b.id, OK)

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", type=int, required=True)
        parse.add(name="name", required=True)
        parse.add(name="desc",type=str)
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        desc = parse.parse_args().get("desc")
        p = Product.get(pid)
        # 验证同一 product name唯一
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        try:
            b = Build(name, pid, g.user.name, desc)
            b.save()
            return jsonify(myResponse(SUCCESS, b.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="id", type=int, required=True)
        id = parse.parse_args().get("id")
        b = Build.get(id)
        try:
            b.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


class ErrorTypeOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid)
        try:
            e = [i.name for i in p.errorTypes_records]
            return jsonify(myResponse(SUCCESS, e, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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
        p = Product.get(pid)
        e = ErrorType.get(eid)
        if e not in p.errorTypes_records:
            return jsonify(myResponse(21, None, f"Product:{pid}  Not included {eid}"))
        if name in [i.name for i in p.builds_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        e.name = name
        e.save()
        return jsonify(SUCCESS, e.id, OK)

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="name")
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid)

        if name in [i.name for i in p.errorTypes_records]:
            return jsonify(myResponse(31, None, f"name:{name} already exists "))
        try:
            e = ErrorType(name, pid)
            e.save()
            return jsonify(myResponse(SUCCESS, e.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="id", type=int, required=True)
        id = parse.parse_args().get("id")
        e = ErrorType.get(id)
        try:
            e.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


class ModuleOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", location='args', required=True)
        pid = parse.parse_args().get("productId")
        p = Product.get(pid)
        try:
            e = [i.name for i in p.modules_records]
            return jsonify(myResponse(SUCCESS, e, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="productId", req_type=int, required=True)
        parse.add(name="name", required=True)
        pid = parse.parse_args().get("productId")
        name = parse.parse_args().get("name")
        p = Product.get(pid)

        if name in [i.name for i in p.modules_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        try:
            m = Module(name, pid)
            m.save()
            return jsonify(myResponse(SUCCESS, m.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="id", type=int, required=True)

        e = Module.get(parse.parse_args().get("id"))
        try:
            e.delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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
        p = Product.get(pid)
        e = Module.get(mid)
        if e not in p.modules_records:
            return jsonify(myResponse(Error_Relation, None, f"Product:{pid}  Not included {mid}"))
        if name in [i.name for i in p.modules_records]:
            return jsonify(myResponse(UNIQUE, None, f"name:{name} already exists "))
        e.name = name
        e.save()
        return jsonify(SUCCESS, e.id, OK)


class ProjectOpt(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name='projectId', required=True)
        p = Project.get(parse.parse_args().get("projectId"))
        try:
            e = [i.name for i in p.product]
            return jsonify(myResponse(SUCCESS, e, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

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
            return jsonify(myResponse(SUCCESS, p.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="id", type=int, required=True)
        id = parse.parse_args().get("id")
        try:
            Project.get(id).delete()
            return jsonify(myResponse(SUCCESS, None, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


api_script = Api(myBug)
api_script.add_resource(ProductOpt, '/productOpt')
api_script.add_resource(SolutionOpt, '/solutionOpt')
api_script.add_resource(BuildOpt, '/buildOpt')
api_script.add_resource(ErrorTypeOpt, '/errorTypeOpt')
api_script.add_resource(PlatformOpt, '/platformOpt')
api_script.add_resource(ModuleOpt, "/moduleOpt")
api_script.add_resource(ProjectOpt, '/projectOpt')
