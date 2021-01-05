# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午2:48
# @Author  : cyq
# @File    : users.py
from flask import jsonify, request, g
from flask_restful import Resource, Api, reqparse
from APP import auth, db
from APP.api import myBug
from .errors_or_auth import myResponse
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

        log.info(f"<login>  account: {account}  password: {password}")

        user = User.query.filter(User.account == account).first()
        if user:
            res = user.verify_password(password)
            if res:
                token = user.generate_auth_token().decode("ascii")
                log.info(f"<login>  generateToken: {token}")
                return jsonify(myResponse(0, token, "ok"))
            else:
                log.error(f"<login>  error password !")
                return jsonify(myResponse(1, None, "err password"))
        log.error(f"<login>  err account !")
        return jsonify(myResponse(1, None, "err account"))


api_script = Api(myBug)
api_script.add_resource(Login, "/login")
