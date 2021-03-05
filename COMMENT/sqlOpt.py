# -*- coding: utf-8 -*-

# @Time    : 2021/3/5 上午10:37
# @Author  : cyq
# @File    : sqlOpt.py

from APP import create_app
from sqlalchemy import create_engine


class SqlOpt:
    eng = create_engine(create_app().config['SQLALCHEMY_DATABASE_URI'], echo=False)

    def __init__(self):
        pass

    def select(self):
        """
        select title, level from bugs where id > 1 and level = 'p1'
        :return:
        """
        pass

    def update(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass


class Argument:

    def __init__(self, table,):
        pass




if __name__ == '__main__':
    a = [{'key': 'id', 'condition': '>', 'val': 1},
         {'key': 'level', 'condition': '=', 'val': 'p1'}]


    table = "bugs"
