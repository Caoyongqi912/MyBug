# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:48
# @Author  : cyq
# @File    : users.py


from flask import jsonify, g
from flask_restful import Resource, Api
from APP import auth
from .errors_or_auth import is_admin
from APP.api import myBug
from COMMENT.myBlinker import login_signal
from COMMENT.ParamParse import MyParse
from COMMENT.const import *

log = get_log(__file__)


class Login(Resource):
    def post(self) -> jsonify:
        parse = MyParse()
        parse.add(name="account", required=True)
        parse.add(name="password", required=True)
        account = parse.parse_args().get("account")
        password = parse.parse_args().get("password")
        user = User.query.filter(User.account == account).first()
        if user:
            res = user.verify_password(password)
            if res:
                token = user.generate_auth_token().decode("ascii")
                # 发送信号
                login_signal.send(username=account)
                info = user.getInfo()
                info['token'] = token

                return jsonify(myResponse(ResponseCode.ResponseCode.SUCCESS, info, ResponseError.OK))
            else:
                return jsonify(myResponse(1, None, "err password"))
        return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.ERROR_ACCOUNT))


@myBug.route("/getToken", methods=["POST"])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    log.info(f"{__name__} get: {token}")
    return jsonify(dict(token=token.decode("ascii")))


class Register(Resource):

    def post(self) -> jsonify:
        """
        注册 post请求
        :return: jsonify
        """
        parse = MyParse()
        parse.add(name="account", required=True)
        parse.add(name="name", required=True)
        parse.add(name="password", required=True)
        parse.add(name="departmentId", type=int, required=False)
        parse.add(name="admin", type=bool, required=False, default=False)
        parse.add(name="gender", type=bool, required=False, default=True)

        departmentId = parse.parse_args().get("departmentId")
        account = parse.parse_args().get("account")
        name = parse.parse_args().get("name")
        password = parse.parse_args().get("password")
        admin = parse.parse_args().get("admin")
        gender = parse.parse_args().get('gender')

        if departmentId:
            # departmentId验证
            Department.get(departmentId, 'departmentId')

        # name 验证
        User.verify_name(name)
        u = User(account=account, name=name, password=password, gender=gender, department=departmentId, admin=admin)
        u.save()

        return jsonify(myResponse(ResponseCode.SUCCESS, u.id, ResponseError.OK))


class DepartmentOpt(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        """
        创建部门
        :return:  jsonify
        """
        parse = MyParse()
        parse.add(name="name", required=True)
        name = parse.parse_args().get("name")
        Department.verify_name(name=name)
        try:
            d = Department(name=name)
            d.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, d.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            db.session.rollback()

            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def put(self) -> jsonify:
        """
        修改部门信息
        :return: jsonify
        """
        parse = MyParse()
        parse.add(name="departmentId", required=True)
        parse.add(name="name", required=True)
        did = parse.parse_args().get("departmentId")
        name = parse.parse_args().get("name")
        d = Department.get(did, 'departmentId')
        try:
            d.name = name
            d.save()
            return jsonify(myResponse(ResponseCode.SUCCESS, d.id, ResponseError.OK))
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        """
        删除部门
        :return: jsonify
        """
        parse = MyParse()
        parse.add(name="id", required=True)

        d = Department.get(parse.parse_args().get("id"), 'departmentId')
        try:
            d.delete()
            return jsonify(myResponse(ResponseCode.SUCCESS, None, ResponseError.OK))
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(ResponseCode.ERROR, None, ResponseError.SOME_ERROR_TRY_AGAIN))


class GetDepartInfo(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        par = MyParse()
        par.add(name="departmentId", required=True, location="args")
        d = Department.get(par.parse_args().get("departmentId"), 'departmentId')
        dInfo = {"name": d.name}
        return jsonify(myResponse(ResponseCode.SUCCESS, dInfo, ResponseError.OK))


class GetUserInfo(Resource):
    @auth.login_required
    def post(self):
        """
        获取用户信息
        :return:
        """
        user = g.user.getInfo()
        return jsonify(myResponse(ResponseCode.SUCCESS, user, ResponseError.OK))

    @auth.login_required
    def get(self):
        user = g.user.getInfo()
        return jsonify(myResponse(ResponseCode.SUCCESS, user, ResponseError.OK))


api_script = Api(myBug)
api_script.add_resource(Login, "/login")
api_script.add_resource(Register, "/register")
api_script.add_resource(DepartmentOpt, "/departmentOpt")
# api_script.add_resource(GetUsers, '/getUsers')
api_script.add_resource(GetUserInfo, "/getUserInfo")
api_script.add_resource(GetDepartInfo, "/getDepartInfo")
