# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:48
# @Author  : cyq
# @File    : users.py


from flask import jsonify, g, request
from flask_restful import Resource, Api, reqparse, inputs
from APP import auth, db
from .errors_or_auth import is_admin
from APP.api import myBug
from COMMENT.myResponse import myResponse
from Model.models import User, Department
from COMMENT.Log import get_log
from COMMENT.myRequestParser import MyRequestParser
from COMMENT.myBlinker import login_signal

log = get_log(__file__)


class Login(Resource):

    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("account", type=str, required=True, help="error account")
        parse.add_argument("password", type=str, required=True, help="error password")

        account = parse.parse_args().get("account")
        password = parse.parse_args().get("password")
        user = User.query.filter(User.account == account).first()
        if user:
            res = user.verify_password(password)
            if res:
                token = user.generate_auth_token().decode("ascii")
                # 发送信号
                login_signal.send(username=account)

                return jsonify(myResponse(0, token, "ok"))
            else:
                log.error(f"<{__class__}>  error password !")
                return jsonify(myResponse(1, None, "err password"))
        log.error(f"<{__class__}>  err account !")
        return jsonify(myResponse(1, None, "err account"))


@myBug.route("/getToken", methods=["POST"])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    log.info(f"{__name__} get: {token}")
    return jsonify(dict(token=token.decode("ascii")))


class Register(Resource):

    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("account", type=str, required=True)
        parse.add_argument("name", type=str, required=True)
        parse.add_argument("password", type=str, required=True)
        parse.add_argument("departmentId", type=str)

        departmentId = parse.parse_args().get("departmentId")
        account = parse.parse_args().get("account")
        name = parse.parse_args().get("name")
        password = parse.parse_args().get("password")

        admin = request.json.get('admin')
        gender = request.json.get('gender')

        if not isinstance(admin, bool):
            return jsonify(myResponse(22, None, "admin typeError"))
        if not isinstance(gender, bool):
            return jsonify(myResponse(22, None, "gender typeError"))
        if departmentId:
            # departmentId验证
            Department.get(departmentId)

        # name 验证
        User.verify_name(name)
        u = User(account=account, name=name, password=password, gender=gender, department=departmentId, admin=admin)
        u.save()

        return jsonify(myResponse(0, u.id, "ok"))


class DepartmentOpt(Resource):

    @auth.login_required
    @is_admin
    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("name", type=str, required=True)

        name = parse.parse_args().get("name")
        Department.verify_name(name=name)
        try:
            d = Department(name=name)
            d.save()
            return jsonify(myResponse(0, d.id, "ok"))
        except Exception as  e:
            log.error(e)
            return jsonify(myResponse(1, None, e))

    @auth.login_required
    @is_admin
    def put(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=True)
        parse.add_argument("name", type=str, required=True)

        did = parse.parse_args().get("id")
        name = parse.parse_args().get("name")
        d = Department.get(did)
        try:
            d.name = name
            d.save()
            return jsonify(myResponse(0, d.id, "ok"))
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(1, None, e))

    @auth.login_required
    @is_admin
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("id", type=str, required=True)
        did = parse.parse_args().get("id")
        d = Department.get(did)
        try:
            d.delete()
            return jsonify(myResponse(0, None, "ok"))
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return jsonify(myResponse(1, None, e))


api_script = Api(myBug)
api_script.add_resource(Login, "/login")
api_script.add_resource(Register, "/register")
api_script.add_resource(DepartmentOpt, "/departmentOpt")
