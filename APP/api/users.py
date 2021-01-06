# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:48
# @Author  : cyq
# @File    : users.py


from flask import jsonify, g
from flask_restful import Resource, Api, reqparse
from APP import auth
from APP.api import myBug
from COMMENT.MyResponse import myResponse
from Model.models import User
from COMMENT.Log import get_log
from COMMENT.myRequestParser import MyRequestParser

log = get_log(__file__)


class Login(Resource):

    def post(self):
        parse = reqparse.RequestParser(argument_class=MyRequestParser)
        parse.add_argument("account", type=str, required=True, help="error account")
        parse.add_argument("password", type=str, required=True, help="error password")

        account = parse.parse_args().get("account")
        password = parse.parse_args().get("password")

        log.info(f"{__class__}  account: {account}  password: {password}")

        user = User.query.filter(User.account == account).first()
        if user:
            res = user.verify_password(password)
            if res:
                token = user.generate_auth_token().decode("ascii")
                log.info(f"{__class__}  generateToken: {token}")
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
        parse.add_argument("admin", type=bool)
        parse.add_argument("department", type=str, required=False)
        parse.add_argument("gender", type=bool, required=False)

        department = parse.parse_args().get("department")
        account = parse.parse_args().get("account")
        name = parse.parse_args().get("name")
        password = parse.parse_args().get("password")
        admin = parse.parse_args().get("admin")
        gender = parse.parse_args().get("gender")

        User.verify_name(name)

        User(account=account, name=name, password=password, gender=gender, department=department, admin=admin).save()

        return jsonify(myResponse(0, None, "ok"))


api_script = Api(myBug)
api_script.add_resource(Login, "/login")
api_script.add_resource(Register, "/register")
