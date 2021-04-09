# -*- coding: utf-8 -*-

# @Time    : 2021/3/5 上午10:37
# @Author  : cyq
# @File    : sqlOpt.py
from flask_restful import abort

from APP import create_app
from sqlalchemy import create_engine

from COMMENT.const import SQL_PARAM_ERROR
from COMMENT.myResponse import myResponse
from COMMENT.Log import get_log

log = get_log(__file__)


class SqlOpt:
    eng = create_engine(create_app().config['SQLALCHEMY_DATABASE_URI'], echo=False)
    condition = ["in", "not in", "=", ">", "<"]

    def __init__(self, table):
        self.table = table

    def select(self, params: list, targets: list = None, opt: str = "and", limit=None):
        """
        select title, level from bugs where id > 1 and level = 'p1'
        :targets:[title, level]
        :params: [{"key":"id",condition:[ ">"|"<"|"=" ],"val":"1"},]
        :return:
        """
        params = self._verify(params)
        if targets:
            sql = f"select {', '.join([k for k in targets])} from {self.table} where "
        else:
            sql = f"select * from {self.table} where "

        for param in params:
            s = " ".join([param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '" ' + f"{opt} "])
            sql += s
        sql = sql.strip(f"{opt} ")
        return self._doSelect(sql, limit)

    def update(self, params: list, targets: list, opt: str = "and")->bool:
        """
        update table set title = 'test' where id =1 and p1
        :params: [{"key":"id",condition:[ ">"|"<"|"=" ],"val":"1"},]
        ;targets [{"key":""title","val":"test"},{"key":"level","val":"p1"}]
        :return:
        """
        params = self._verify(params)
        tar = ""
        for i in targets:
            tar += i["key"]
            tar += " = "
            tar += f"'{i['val']}'"
            tar += ", "
        tar = tar.strip(", ")
        sql = f"update {self.table} set {tar} where "
        if len(params) > 1:
            for param in params:
                s = " ".join([param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '" ' + f"{opt} "])
                sql += s
            sql = sql.strip(f"{opt} ")
        else:
            param = params[0]
            s = " ".join([param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '"'])
            sql += s

        try:
            self.eng.execute(sql)
            log.debug(f"sql: {sql}")
            return True
        except Exception as e:
            log.error(e)
            return False

    def insert(self):
        """
        insert into table values (val1,val2)
        insert into table (const1,const2) values (val1,val2)
        :return:
        """

    def delete(self):
        """
        delete from table where k=v
        :return:
        """

    def _doSelect(self, sql, limit) -> list:
        try:
            res = self.eng.execute(sql)
            log.debug(f"sql: {sql}")
            if limit:
                return res.fetchmany(limit)
            else:
                return res.fetchall()
        except Exception as e:
            log.error(e)
            return []

    def _verify(self, body: list) -> list:
        for b in body:
            if not b.get("key") and not b.get("condition") and not b.get("val"):
                abort(myResponse(SQL_PARAM_ERROR, None, "invalid params"))

            if b.get("condition") not in self.condition:
                abort(myResponse(SQL_PARAM_ERROR, None, f"{b.get['condition']}  is  invalid "))
        return body


if __name__ == '__main__':
    opt = [{'key': 'id', 'condition': '>', 'val': 1},
           {'key': 'level', 'condition': '=', 'val': 'p2'}]
    targets = ['title']
    from Model.models import User

    put_targets = [{"key": "title", "val": "test"}, {"key": "level", "val": "p1"}]
    put_opt =[{'key': 'id', 'condition': '=', 'val': 1}]
    # a = SqlOpt("bugs").select(opt, targets)
    SqlOpt('bugs').update(put_opt, put_targets)
