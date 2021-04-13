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
            sql = f"SELECT {', '.join([k for k in targets])} FROM {self.table} WHERE "
        else:
            sql = f"SELECT * FROM {self.table} WHERE "

        for param in params:
            s = " ".join(
                [param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '" ' + f"{opt} ".upper()])
            sql += s
        sql = sql.rstrip(f"{opt} ".upper())
        return self._doSelect(sql, limit)

    def update(self, params: list, targets: list, opt: str = "and") -> bool:
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
        sql = f"UPDATE {self.table} SET {tar} WHERE "
        if len(params) > 1:
            for param in params:
                s = " ".join(
                    [param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '" ' + f"{opt} ".upper()])
                sql += s
            sql = sql.rstrip(f"{opt} ".upper())
        else:
            param = params[0]
            s = " ".join([param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '"'])
            sql += s

        try:
            self.eng.execute(sql)
            log.info(f"sql: {sql}")
            return True
        except Exception as e:
            log.error(e)
            return False

    def insert(self, params: list):
        """
        insert into table values (val1,val2)
        insert into table (const1,const2) values (val1,val2)
        :param [{"key":"name","val":"cyq"]
        :return:
        """
        const = list()
        values = list()

        for param in params:
            const.append(param['key'])
            values.append(f"'{str(param['val'])}'")
        sql = f"INSERT INTO {self.table} ({','.join(const)}) VALUES ({','.join(values)})  "
        try:
            self.eng.execute(sql)
            log.info(f"sql: {sql}")
            return True
        except Exception as e:
            print(e)
            log.error(e)
            return False

    def delete(self, params: list, opt: str = "") -> bool:
        """
        delete from table where k=v
        :params: [{"key":"id",condition:[ ">"|"<"|"=" ],"val":"1"},]
        :opt : AND OR None
        :return:
        """
        sql = f"DELETE FROM {self.table} WHERE "
        params = self._verify(params)
        for param in params:
            s = " ".join(
                [param.get("key"), param.get("condition"), '"' + str(param.get('val')) + '" ' + f"{opt} ".upper()])
            sql += s

        sql = sql.rstrip(f"{opt} ".upper())

        try:
            self.eng.execute(sql)
            log.info(f"sql: {sql}")
            return True
        except Exception as e:
            print(e)
            log.error(e)
            return False

    def _doSelect(self, sql, limit) -> list:
        try:
            res = self.eng.execute(sql)
            log.info(f"sql: {sql}")
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
    put_opt = [{'key': 'id', 'condition': '=', 'val': 1}]

    delPar = [{"key": "id", "val": 1, "condition": "="}]
    delOpt = "AND"

    # a = SqlOpt("bugs").select(opt, targets)
    # SqlOpt('bugs').update(put_opt, put_targets)
    # SqlOpt("bugs").delete(delPar)
    import time

    insertPar = [{"key": "name", "val": "test"}, {"key": "create_time", "val": time.time()}]
    SqlOpt("project").insert(insertPar)
