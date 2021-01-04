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
    gender = db.Column(db.Enum(True, False), server_default=True, comment="性别")
    admin = db.Column(db.Enum(True, False), server_default=True, default=False, comment="管理员")
    department = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

    def __init__(self, account, name, password, gender, department, admin=None):
        self.account = account
        self.name = name
        self.password = password
        self.gender = gender
        self.admin = admin
        self.department = department


class Bugs(Base):
    __tablename__ = "bugs"
    title = db.Column(db.String(100), index=True, comment="BUG标题")
    level = db.Column(db.Enum(1, 2, 3, 4), comment='BUG严重等级')
    priority = db.Column(db.Enum(1, 2, 3, 4), comment="BUG优先级")
    status = db.Column(db.Enum("ACTIVE", "RESOLVED", "CLOSED"), comment="BUG状态")
    confirmed = db.Column(db.Enum(True, False), comment="是否确认")
    creater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="创建者")
    updater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="修改者")
    assignedTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="指派给")
    resolvedBy = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="解决者")
    resolution = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="解决状态")
    mailTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="指派给")
    stepsBody = db.Column(db.TEXT, comment="步骤")

    def __init__(self,title,level,priority,status,confirmed,creater,updater,assignedTo,resolvedBy,
                 resolution,mailTo,stepsBody):
        self.title = title
        self.level = level
        self.priority = priority
        self.status = status
        self.confirmed = confirmed
        self.creater = creater
        self.updater = updater
        self.assignedTo = assignedTo
        self.resolution = resolution
        self.resolvedBy = resolvedBy
        self.mailTo = mailTo
        self.stepsBody = stepsBody

