# -*- coding: utf-8 -*-

# @Time    : 2021/1/5 下午3:18
# @Author  : cyq
# @File    : myRequestParser.py


from flask_restful import reqparse, current_app, abort


class MyRequestParser(reqparse.Argument):
    """
        继承自 reqparse.Argument, 增加 nullable 关键字参数，
        对于值为 None 并且 nullable=False 的字段 raise TypeError
        """

    def __init__(self, name, default=None, dest=None, required=False, ignore=False, type=reqparse.text_type,
                 location=('json', "value"), choices=(), action="store", help=None, operators=('=',),
                 case_sensitive=True, nullable=False):
        self.nullable = nullable
        super(MyRequestParser, self).__init__(name, default=default, dest=dest,
                                              required=required, ignore=ignore,
                                              type=type, location=location,
                                              choices=choices, action=action,
                                              help=help,
                                              operators=operators,
                                              case_sensitive=case_sensitive)

    def convert(self, value, op):
        """
        重写convert
        加入判断是否为空
        :param value:
        :param op:
        :return:
        """

        if value is None or value == "":
            raise TypeError(f"{value} can't be null!")
        return super(MyRequestParser, self).convert(value, op)

    def handle_validation_error(self, error, bundle_errors):
        """
        自定义错误返回
        :param error:
        :param bundle_errors:
        :return:
        """
        err = f"{self.name} 非法参数！"
        print(error)
        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, err
        abort(400, code=1, data=None, msg=err)
