# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午5:43
# @Author  : cyq
# @File    : models.py

import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import current_app, abort
from sqlalchemy import desc
from APP import db
from COMMENT.Log import get_log
from COMMENT.myResponse import myResponse

log = get_log(__file__)


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

    @classmethod
    def get(cls, id, parseName):
        return cls.query.get_or_NoFound(id, parseName)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()

    @classmethod
    def verify_name(cls, name):
        """同名校验"""
        res = cls.query.filter_by(name=name).first()
        if res:
            abort(myResponse(1, None, f"{name} already exists"))


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
    account = db.Column(db.String(20), comment="用户名")
    name = db.Column(db.String(20), unique=True, comment="真实姓名")
    password = db.Column(db.String(50), comment="密码")
    gender = db.Column(db.Boolean, default=True, comment="性别")
    admin = db.Column(db.Boolean, default=False, comment="管理员")
    department = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

    myNote = db.relationship("Note", backref="userNote", lazy='dynamic')  # 我的备注

    def __init__(self, account, name, password, gender, department, admin=None):
        self.account = account
        self.name = name
        self.gender = gender
        self.admin = admin
        self.department = department
        self.hash_password(password)

    def get_uid(self):
        """get id"""
        return self.id

    @classmethod
    def getUsers(cls) -> list:
        """返回所有用户"""
        return [{
            "uid": info.id,
            "account": info.account,
            "name": info.name,
            "department": info.department,
            "ctime": info.create_time,
            "role": "admin " if info.admin else "editor"

        } for info in cls.all()]

    @classmethod
    def get(cls, id, parseName, obj=True):
        user = super(User, cls).get(id, parseName)
        if obj:
            return user
        else:
            info = {
                "uid": user.id,
                "account": user.account,
                "name": user.name,
                "department": user.department,
                "ctime": user.create_time,
                "role": 1 if user.admin else 0
            }
            return info

    @property
    def getName(self):
        return self.name

    def getInfo(self):
        return {"id": self.id, "name": self.name, "department": self.department,
                "ctime": self.create_time, "role": "admin" if self.admin else "editor"}

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

        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_time},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """
        token 验证
        :param token: token
        :return: user
        """
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=["HS256"])
        except:
            return None

        return User.query.get(data['id'])

    def __repr__(self):
        return f"User: {self.name}"


class Project(Base):
    """项目类"""
    __tablename__ = "project"
    name = db.Column(db.String(30), unique=True, comment="项目名")
    product = db.relationship("Product", backref="project", lazy="dynamic", cascade="save-update,delete")

    def __init__(self, name):
        self.name = name

    @classmethod
    def get(cls, id, parseName, obj=True):
        pro = super(Project, cls).get(id, parseName)
        if obj:
            return pro
        else:
            info = {
                "name": pro.name,
            }
            return info

    @property
    def product_records(self):
        return self.product.filter_by().all()

    def __repr__(self):
        return f"project: {self.name}"


class Product(Base):
    """产品类"""
    __tabelname__ = "product"
    name = db.Column(db.String(50), unique=True, comment="产品名")
    # 所有解决方案
    solutions = db.relationship("Solution", backref="product_solutions", lazy="dynamic", cascade="save-update,delete")
    # 所有测试平台
    platforms = db.relationship("Platform", backref="product_platforms", lazy="dynamic", cascade="save-update,delete")
    # 所有版本
    builds = db.relationship("Build", backref="product_builds", lazy="dynamic", cascade="save-update,delete")
    # 所有错误类型
    errorTypes = db.relationship("ErrorType", backref="product_error_types", lazy="dynamic",
                                 cascade="save-update,delete")
    # 所有bug
    bugs = db.relationship("Bugs", backref="product_bugs", lazy="dynamic")
    # 所属项目
    projectId = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False, comment='所属项目')

    # 所有模块
    modules = db.relationship("Module", backref="product_modules", lazy="dynamic", cascade="save-update,delete")

    def __init__(self, name, projectId):
        self.projectId = projectId
        self.name = name

    @classmethod
    def get(cls, id, parseName, obj=True):
        pro = super(Product, cls).get(id, parseName)
        if obj:
            return pro
        else:
            info = {
                "name": pro.name,
                "ctime": pro.create_time
            }

            return info

    @classmethod
    def getBugs(cls, id, name):
        pro = super(Product, cls).get(id, name)

        info = {
            "name": pro.name,
            "ctime": pro.create_time,
            "bugs": pro.bugs_records

        }
        return info

    @property
    def modules_records(self) -> list:
        return self.modules.filter_by().all()

    @property
    def bugs_records(self):
        bugInfo = [{
            "bugID": bug.id,
            "createTime": bug.create_time,
            "title": bug.title,
            "level": bug.level,
            "priority": bug.priority,
            "status": bug.status,
            "confirmed": bug.confirmed,
            "creater": bug.creater,
            "updater": bug.updater,
            "assignedTo": bug.assignedTo,
            "resolvedBy": bug.resolvedBy,
        } for bug in self.bugs.all()]
        return bugInfo

    @property
    def solutions_records(self):
        return self.solutions.filter_by().all()

    @property
    def platforms_records(self):
        return self.platforms.filter_by().all()

    @property
    def builds_records(self):
        return self.builds.filter_by().all()

    @property
    def projects_records(self):
        return self.projects.filter_by().all()

    @property
    def errorTypes_records(self):
        return self.errorTypes.filter_by().all()

    def __repr__(self):
        return f"product {self.name}"


class Solution(Base):
    """解决方案类"""
    __tablename__ = "solution"
    name = db.Column(db.String(30), unique=False, comment="解决方案名")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="solution_bugs", lazy='dynamic')

    def __init__(self, name, productId):
        self.name = name
        self.product = productId

    def __repr__(self):
        return f"resolved: {self.name}"


class Platform(Base):
    """所用平台类"""
    __tablename__ = "platform"
    name = db.Column(db.String(30), unique=False, comment="平台名称")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="platform_bugs", lazy='dynamic')

    def __init__(self, name, productId):
        self.name = name
        self.product = productId

    def __repr__(self):
        return f"platform: {self.name}"


class Build(Base):
    """所用版本类"""
    __tablename__ = "build"
    name = db.Column(db.String(30), unique=False, comment="版本编号")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="build_bugs", lazy='dynamic')
    builder = db.Column(db.String(20), comment="构建者")
    desc = db.Column(db.String(50), comment="描述")

    def __init__(self, name, productId, builder, desc=None):
        self.name = name
        self.product = productId
        self.builder = builder
        self.desc = desc

    @classmethod
    def get(cls, id, name, obj=True):
        build = super(Build, cls).get(id, name)
        if obj:
            return build
        else:
            info = {
                "name": build.name,
                "builder": build.builder,
                "desc": build.desc,
                "ctime": build.create_time

            }
            return info

    def __repr__(self):
        return f"build: {self.name}"


class ErrorType(Base):
    """错误类型类"""
    __tablename__ = "error_type"
    name = db.Column(db.String(30), unique=False, comment="错误类型")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, comment='所属产品')
    bugs = db.relationship("Bugs", backref="error_type_bugs", lazy='dynamic')

    def __init__(self, name, productId):
        self.name = name
        self.product = productId

    def __repr__(self):
        return f"error_type: {self.name}"


class Module(Base):
    """bug模块类"""
    __tablename__ = "module"
    name = db.Column(db.String(30), unique=False, comment="模块名")
    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True, comment='所属产品')
    bugs = db.relationship("Bugs", backref="model_bugs", lazy='dynamic')

    def __init__(self, name, productId):
        self.name = name
        self.product = productId

    def __repr__(self):
        return f"module: {self.name}"


class BugFile(Base):
    """bug 文件"""
    __tablename__ = "bug_file"
    fileName = db.Column(db.String(60), comment="文件名")
    filePath = db.Column(db.String(100), comment="文件地址")
    bugID = db.Column(db.Integer, db.ForeignKey("bugs.id"), comment="所属bug")

    def __init__(self, fileName, filePath, bugID):
        self.fileName = fileName
        self.filePath = filePath
        self.bugID = bugID

    def __repr__(self):
        return f"fileName: {self.fileName}"


class Bugs(Base):
    """bug类"""
    __tablename__ = "bugs"
    title = db.Column(db.String(100), index=True, comment="BUG标题")
    level = db.Column(db.Enum("p1", "p2", "p3", "p4"), server_default="p3", comment='BUG严重等级')
    priority = db.Column(db.Enum("p1", "p2", "p3", "p4"), server_default="p3", comment="BUG优先级")
    status = db.Column(db.Enum("ACTIVE", "RESOLVED", "CLOSED"), server_default="ACTIVE", comment="BUG状态")
    confirmed = db.Column(db.Boolean, default=False, comment="是否确认")

    creater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="创建者ID")
    createrName = db.Column(db.String(32), comment="创建者姓名")
    updater = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="修改者")
    updaterName = db.Column(db.String(32), nullable=True, comment="修改者姓名")

    assignedTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="指派给")
    resolvedBy = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="解决者")
    mailTo = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, comment="抄送给")

    stepsBody = db.Column(db.TEXT, comment="步骤")
    solution = db.Column(db.Integer, db.ForeignKey("solution.id"), nullable=True, comment="解决方案")
    platform = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=True, comment="测试平台")
    module = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=True, comment="所属模块")

    product = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True, comment="所属项目")
    build = db.Column(db.Integer, db.ForeignKey("build.id"), nullable=False, comment="版本")
    errorType = db.Column(db.Integer, db.ForeignKey("error_type.id"), nullable=True, comment="错误类型")

    bugFile = db.relationship('BugFile', backref="bug_file", lazy='dynamic')

    def __init__(self, title, creater, stepsBody, product, build):
        self.title = title
        self.creater = creater
        self.stepsBody = stepsBody
        self.build = build
        self.product = product

    def __repr__(self):
        return f"bug: {self.title}"

    @classmethod
    def get(cls, id, parse, obj=True):
        bug = super(Bugs, cls).get(id, parse)
        if obj:
            return bug
        else:
            bugInfo = {
                "bugID": bug.id,
                "createTime": bug.create_time,
                "title": bug.title,
                "level": bug.level,
                "priority": bug.priority,
                "status": bug.status,
                "confirmed": bug.confirmed,
                "creater": bug.creater,
                "updater": bug.updater,
                "creatername": bug.createrName,
                "updaterName": bug.updaterName,
                "assignedTo": bug.assignedTo,
                "resolvedBy": bug.resolvedBy,
                "mailTo": bug.mailTo,
                "stepsBody": bug.stepsBody,
                "solutionID": bug.solution,
                "platformID": bug.platform,
                "productID": bug.product,
                "buildID": bug.build,
                "errorTypeID": bug.errorType,
                "module": bug.module,
                "bugFiles": bug.myFiles()

            }
            return bugInfo

    def myFiles(self):
        """
        [{fileName:xxx,filePath:xxx}]
        """
        return [{"id": f.id, "fileName": f.fileName, "filePath": f.filePath} for f in self.bugFile.filter_by().all()]

    def updateBug(self, updateBody: dict):
        """数据更新"""
        try:
            if updateBody.get("module"):
                self.module = updateBody.get("module")

            if updateBody.get("title"):
                self.title = updateBody.get("title")

            if updateBody.get("level"):
                self.level = updateBody.get("level")

            if updateBody.get("priority"):
                self.priority = updateBody.get("priority")

            if updateBody.get("status"):
                self.status = updateBody.get("status")

            if updateBody.get("confirmed"):
                self.confirmed = updateBody.get("confirmed")

            if updateBody.get("platformId"):
                self.platform = updateBody.get("platformId")

            if updateBody.get("buildId"):
                self.build = updateBody.get("buildId")

            if updateBody.get("errorTypeId"):
                self.errorType = updateBody.get("errorTypeId")

            if updateBody.get("assignedTo"):
                self.assignedTo = updateBody.get("assignedTo")

            if updateBody.get("mailTo"):
                self.mailTo = updateBody.get("mailTo")

            if updateBody.get("stepsBody"):
                self.stepsBody = updateBody.get("stepsBody")

            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            abort(myResponse(1, None, e))

    @classmethod
    def optGetBugInfos(cls, opt) -> list:
        from flask import g

        if opt == "all":
            return Bugs.all()
        elif opt == "unClose":
            return Bugs.query.filter(Bugs.status == "CLOSED").order_by(desc(Bugs.id)).all()
        elif opt == "createByMe":
            return Bugs.query.filter(Bugs.creater == g.user.id).order_by(desc(Bugs.id)).all()
        elif opt == "assignedToMe":
            return Bugs.query.filter(Bugs.assignedTo == g.user.id).order_by(desc(Bugs.id)).all()
        elif opt == "resolvedByMe":
            return Bugs.query.filter(Bugs.resolvedBy == g.user.id).order_by(desc(Bugs.id)).all()


class Note(Base):
    __tablename__ = "note"

    bug = db.Column(db.Integer, db.ForeignKey("bugs.id"), nullable=False, comment="所属bug")
    content = db.Column(db.TEXT, comment="备注内容")
    noteMan = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="备注人")

    def __init__(self, bugID: int, content: str, noteMan: int):
        self.bug = bugID
        self.content = content
        self.noteMan = noteMan

    def __repr__(self):
        return f"bugID: {self.bug}, note:{self.content}"


class BugModel(Base):
    """bug模版"""
    __tablename__ = "bug_model"
    name = db.Column(db.String(32), unique=False, comment="bug模版")
    content = db.Column(db.TEXT, comment="模版内容")

    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content
