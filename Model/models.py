# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:43
# @Author  : cyq
# @File    : models.py

import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import current_app
from sqlalchemy import desc
from APP import db


class Base(db.Model):
    """
    model 基类
    """
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
    """部门类"""
    __tablename__ = "department"
    name = db.Column(db.String(20), unique=True, comment="部门名")
    users = db.relationship("User", backref="user_part", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"departmentName: {self.name}"


class User(Base):
    """
    用户类
    """
    __tablename__ = "user"
    account = db.Column(db.String(20), comment="真实姓名")
    name = db.Column(db.String(20), unique=True, comment="用户名")
    password = db.Column(db.String(50), comment="密码")
    gender = db.Column(db.Boolean, default=True, comment="性别")
    admin = db.Column(db.Boolean, default=False, comment="管理员")
    department = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

    def __init__(self, account, name, password, gender, department, admin=None):
        self.account = account
        self.name = name
        self.password = password
        self.gender = gender
        self.admin = admin
        self.department = department

    def is_superuser(self) -> bool:
        """是否是管理员"""
        return self.admin

    def hash_password(self, password):
        """密码哈希"""
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_time=100 * 1000):
        """
        生产token
        :param expires_time: 过期时间
        :return: token
        """

        return jwt.encode({"id": self.id, "epx": time.time() + expires_time},
                          current_app.config['SECRET_KEY'], algorithms=["HS256"])




    @staticmethod
    def verify_token(token):
        """
        token 验证
        :param token: token
        :return: user
        """
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return None

        return User.query.get(data['id'])

    def __repr__(self):
        return f"User: {self.name}"


class Product(Base):
    """产品类"""
    __tabelname__ = "product"
    name = db.Column(db.String(50), unique=True, comment="产品名")
    # 所有解决方案
    solutions = db.relationship("Solution", backref="product_solutions", lazy="dynamic")
    # 所有测试平台
    platforms = db.relationship("Platform", backref="product_platforms", lazy="dynamic")
    # 所有版本
    builds = db.relationship("Build", backref="product_builds", lazy="dynamic")
    # 所有错误类型
    errorTypes = db.relationship("ErrorType", backref="product_error_types", lazy="dynamic")
    # 所有bug
    bugs = db.relationship("Bugs", backref="product_bugs", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"product {self.name}"


class Solution(Base):
    """解决方案类"""
    __tablename__ = "solution"
    name = db.Column(db.String(30), unique=True, comment="解决方案名")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="solution_bugs", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"resolved: {self.name}"


class Platform(Base):
    """所用平台类"""
    __tablename__ = "platform"
    name = db.Column(db.String(30), unique=True, comment="平台名称")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="platform_bugs", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"platform: {self.name}"


class Build(Base):
    """所用版本类"""
    __tablename__ = "build"
    name = db.Column(db.String(30), unique=True, comment="版本编号")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="build_bugs", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"build: {self.name}"


class ErrorType(Base):
    """错误类型类"""
    __tablename__ = "error_type"
    name = db.Column(db.String(30), unique=True, comment="错误类型")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="error_type_bugs", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"error_type: {self.name}"


class Bugs(Base):
    """bug类"""
    __tablename__ = "bugs"
    title = db.Column(db.String(100), index=True, comment="BUG标题")
    level = db.Column(db.Enum("p1", "p2", "p3", "p4"), server_default="p3", comment='BUG严重等级')
    priority = db.Column(db.Enum("p1", "p2", "p3", "p4"), server_default="p3", comment="BUG优先级")
    status = db.Column(db.Enum("ACTIVE", "RESOLVED", "CLOSED"), server_default="ACTIVE", comment="BUG状态")
    confirmed = db.Column(db.Boolean, default=False, comment="是否确认")
    creater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="创建者")
    updater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="修改者")
    assignedTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="指派给")
    resolvedBy = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="解决者")
    mailTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="指派给")
    stepsBody = db.Column(db.TEXT, comment="步骤")
    solution = db.Column(db.Integer, db.ForeignKey("solution.id"), nullable=True, comment="解决方案")
    platform = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=True, comment="测试平台")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True, comment="所属项目")
    build = db.Column(db.Integer, db.ForeignKey("build.id"), nullable=False, comment="版本")
    errorType = db.Column(db.Integer, db.ForeignKey("error_type.id"), nullable=True, comment="错误类型")

    def __init__(self, title, creater, stepsBody, product, build, level=None, priority=None, status=None,
                 confirmed=None, updater=None,
                 assignedTo=None, resolvedBy=None, mailTo=None, solution=None, platform=None):
        self.title = title
        self.level = level
        self.priority = priority
        self.status = status
        self.confirmed = confirmed
        self.creater = creater
        self.updater = updater
        self.assignedTo = assignedTo
        self.solution = solution
        self.resolvedBy = resolvedBy
        self.mailTo = mailTo
        self.stepsBody = stepsBody
        self.build = build
        self.product = product
        if not platform:
            self.platform = 0
        else:
            self.platform = platform
