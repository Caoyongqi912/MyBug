# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:43
# @Author  : cyq
# @File    : models.py

import time
from sqlalchemy import desc

from APP import db


class Base(db.Model):
    DELETE_STATUS = 0
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Integer, default=int(time.time()))
    update_time = db.Column(db.Integer, default=int(time.time()), onupdate=int(time.time()))
    status = db.Column(db.SmallInteger, default=1)

    @classmethod
    def all(cls):
        return cls.query.filter_by().order_by(desc(cls.id)).all()


class Department(Base):
    __tablename__ = "department"
    name = db.Column(db.String(20), unique=True, comment="部门名")
    users = db.relationship("User", backref="user_part", lazy="dynamic")

    def __init__(self, name):
        """
        初始化
        :param name:
        """
        self.name = name

    def __repr__(self):
        return f"departmentName: {self.name}"


class User(Base):
    __tablename__ = "user"
    account = db.Column(db.String(20), comment="真实姓名")
    name = db.Column(db.String(20), unique=True, comment="用户名")
    password = db.Column(db.String(50), comment="密码")
    gender = db.Column(db.Boolean, default=True, comment="性别")
    admin = db.Column(db.Boolean, default=False, comment="管理员")
    department = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

