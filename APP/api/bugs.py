# -*- coding: utf-8 -*-

# @Time    : 2021/1/11 下午4:41
# @Author  : cyq
# @File    : bugs.py

from flask_restful import Api, Resource, marshal_with
from sqlalchemy.orm import session

from APP import auth, create_app
from flask import g, jsonify, request
from COMMENT.const import *
from Model.models import *
from APP.api import myBug
from bugFiles.savefile import getFilePath
from .errors_or_auth import is_admin
from COMMENT.Log import get_log
from COMMENT.myResponse import myResponse
from COMMENT.ParamParse import MyParse, SearchParamsParse

log = get_log(__file__)


class MyBugs(Resource):



    @auth.login_required
    def post(self) -> jsonify:
        """
        增加一个bug信息
        :return: jsonify
        """
        parse = MyParse()
        parse.add(name="productId", type=int, required=True)
        parse.add(name="projectId", type=int, required=True)
        parse.add(name="platformId", type=int)
        parse.add(name="buildId", type=int)
        parse.add(name="errorTypeId", type=int)
        parse.add(name="title", required=True)
        parse.add(name="level", choices=['p1', 'p2', 'p3', 'p4'], required=True)
        parse.add(name="priority", choices=['p1', 'p2', 'p3', 'p4'], required=True)
        parse.add(name="assignedTo", type=int, required=True)
        parse.add(name="mailTo", type=int)
        parse.add(name="stepsBody")

        productId = parse.parse_args().get("productId")
        projectId = parse.parse_args().get("projectId")
        platformId = parse.parse_args().get("platformId")
        buildId = parse.parse_args().get("buildId")
        title = parse.parse_args().get("title")
        level = parse.parse_args().get("level")
        priority = parse.parse_args().get("priority")
        assignedTo = parse.parse_args().get("assignedTo")
        mailTo = parse.parse_args().get("mailTo")
        stepsBody = parse.parse_args().get("stepsBody")

        project = Project.get(projectId, "projectId")
        product = Product.get(productId, "productId")

        if mailTo:
            User.get(mailTo, "mailTo")
        if assignedTo:
            User.get(assignedTo, "assignedTo")

        if product not in project.product_records:
            return jsonify(myResponse(Error_Relation, None, f"Project： Not included productId {productId}"))
        if platformId not in [i.id for i in product.platforms_records]:
            return jsonify(myResponse(Error_Relation, None, f"Product： Not included platformId {platformId}"))
        if buildId not in [i.id for i in product.builds_records]:
            return jsonify(myResponse(Error_Relation, None, f"Product： Not included buildId {buildId}"))

        try:
            u = Bugs(title=title, creater=g.user.id, stepsBody=stepsBody, product=productId, build=buildId)
            u.priority = priority
            u.level = level
            u.createrName = g.user.name
            u.save()
            return jsonify(myResponse(SUCCESS, u.id, "ok"))
        except ErrorType as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, str(e)))

    @auth.login_required
    def put(self) -> jsonify:

        parse = MyParse()
        parse.add(name="bugID", type=int, required=True)
        parse.add(name="productId", type=int)
        parse.add(name="projectId", type=int)
        parse.add(name="platformId", type=int)
        parse.add(name="buildId", type=int)
        parse.add(name="errorTypeId", type=int)
        parse.add(name="title")
        parse.add(name="level", choices=['p1', 'p2', 'p3', 'p4'])
        parse.add(name="priority", choices=['p1', 'p2', 'p3', 'p4'])
        parse.add(name="assignedTo", type=int)
        parse.add(name="mailTo", type=int)
        parse.add(name="stepsBody")
        parse.add(name="confirmed", type=bool)
        parse.add(name="status", choices=["ACTIVE", "RESOLVED", "CLOSED"])

        bugID = parse.parse_args().get("bugID")
        projectId = parse.parse_args().get("projectId")
        productId = parse.parse_args().get("productId")
        mailTo = parse.parse_args().get("mailTo")
        assignedTo = parse.parse_args().get("assignedTo")
        platformId = parse.parse_args().get("platformId")
        buildId = parse.parse_args().get("buildId")

        if projectId or productId:
            if not productId:
                return jsonify(myResponse(ERROR, None, cantEmpty("productId")))
            if not projectId:
                return jsonify(myResponse(ERROR, None, cantEmpty("projectId")))
            project = Project.get(projectId, "projectId")
            product = Product.get(productId, "productId")
            if product not in project.product_records:
                return jsonify(myResponse(Error_Relation, None, f"Project： Not included productId {productId}"))
            if product not in project.product_records:
                return jsonify(myResponse(Error_Relation, None, f"Project： Not included productId {productId}"))
            if platformId not in [i.id for i in product.platforms_records]:
                return jsonify(myResponse(Error_Relation, None, f"Product： Not included platformId {platformId}"))

            if buildId not in [i.id for i in product.builds_records]:
                return jsonify(myResponse(Error_Relation, None, f"Product： Not included buildId {buildId}"))

        if mailTo:
            User.get(mailTo, "mailTo")
        if assignedTo:
            User.get(assignedTo, "assignedTo")

        bug = Bugs.get(bugID, "bugID")
        bug.updater = g.user.id
        bug.updaterName = g.user.name
        bug.updateBug(parse.parse_args())

        return jsonify(myResponse(SUCCESS, bug.id, OK))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        parse = MyParse()
        parse.add(name="bugID", type=int, required=True)
        bugID = parse.parse_args().get("bugID")
        bug = Bugs.get(bugID, "bugID")
        bug.delete()

        return jsonify(myResponse(0, None, "ok"))


class BugLists(Resource):

    @auth.login_required
    def get(self):
        par = MyParse()
        par.add(name="productID", required=True, location="args")
        bugInfo = Product.getBugs(par.parse_args().get("productID"), "productID")
        return jsonify(myResponse(SUCCESS, bugInfo, OK))


class MyBug(Resource):

    @auth.login_required
    def get(self) -> jsonify:
        parse = MyParse()
        parse.add(name="bugID", location="args")
        bugID = parse.parse_args().get("bugID")
        bug = Bugs.get(bugID, "bugID", obj=False)

        return jsonify(myResponse(0, bug, "ok"))

    @auth.login_required
    @is_admin
    def delete(self) -> jsonify:
        """
        删除bug接口
        :return:
        """
        parse = MyParse()
        parse.add(name="bugID", type=int, required=True)

        bug = Bugs.get(parse.parse_args().get("bugID"), "bugID")
        bug.delete()
        return jsonify(myResponse(0, None, "ok"))


class Confirmed(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        """
        确认bug接口
        :return:
        """
        parse = MyParse()
        parse.add(name="bugID", type=int, required=True)
        parse.add(name="assignedTo", type=int, required=True)
        parse.add(name="errorType", type=int, required=True)
        parse.add(name="priority")
        parse.add(name="mailTo")
        parse.add(name="note")

        bugID = parse.parse_args().get("bugID")

        bug = Bugs.get(bugID, "bugID")
        bug.update(parse.parse_args())

        return jsonify(myResponse(0, bug.id, "ok"))


class Assigned(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        """
        指派bug
        :return:
        """
        parse = MyParse()
        parse.add(name="bugID", type=int, required=True)
        parse.add(name="assignedTo", type=int, required=True)
        parse.add(name="mailTo")
        parse.add(name="note")

        bugID = parse.parse_args().get("bugID")
        assTo = parse.parse_args().get("assignedTo")
        note = parse.parse_args().get("note")
        User.get(assTo, "assignedTo")
        bug = Bugs.get(bugID, "bugID")

        bug.update(parse.parse_args())

        if note:
            no = Note(bugID, note, g.user.id)
            no.save()

        return jsonify(myResponse(0, bug.id, "ok"))


class CloseBug(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        """
        解决bug
        :return:
        """
        parse = MyParse()
        parse.add(name='bugID', type=int, required=True)
        parse.add(name="confirm", type=int, required=True)
        parse.add(name="errorType", type=int)
        parse.add(name="mailTo", type=int)
        parse.add(name="priority", type=int, required=True)
        parse.add(name="note")

        bugID = parse.parse_args().get('bugID')
        note = parse.parse_args().get("note")

        bug = Bugs.get(bugID, "bugID")
        bug.update(parse.parse_args())

        if note:
            no = Note(bugID, note, g.user.id)
            no.save()

        return jsonify(myResponse(0, bug.id, "ok"))


class CopyBug(Resource):

    @auth.login_required
    def post(self):
        """
        复制bug接口
        :return:
        """

        parse = MyParse()

        parse.add(name="bugID", type=int, required=True)
        bugID = parse.parse_args().get("bugID")
        bug = Bugs.get(bugID, "bugID", obj=False)
        return jsonify(myResponse(SUCCESS, bug, OK))


class SearchBug(Resource):

    @auth.login_required
    def post(self):
        """
        条件查询
        :title 包含  不包含  =   ！=
        :id            = !=
        :assignedTo    = !=
        :creater       = !=
        :resolvedBy    = !=
        :solution      = !=
        :platform      = !=
        :level         = !=
        :priority      = !=
        :status        = !=
        :confirmed     = !=
        :errorType     = !=
        :createTime    = !=


        :return:
        """

        requestBody = {
            "option": "and",
            "searchBody": [
                {
                    "key": "id",
                    "condition": ">",
                    "val": 1
                }, {
                    "key": "level",
                    "condition": "=",
                    "val": "p1"
                }
            ]
        }

        parse = MyParse()
        parse.add(name="option", choices=['and', 'or'], required=True)
        parse.add(name="searchBody", type=list, required=True)
        bugInfos = [{
            "bugID": info[0],
            "createTime": info[1],
            "title": info[3],
            "level": info[4],
            "priority": info[5],
            "status": info[6],
            "confirmed": info[7],
            "creater": info[8],
            "updater": info[1],
            "solutionID": info[14]
        } for info in
            SearchParamsParse(parse.parse_args().get("searchBody"), parse.parse_args().get("option")).filter()]

        return jsonify(myResponse(0, bugInfos, "ok"))

    @auth.login_required
    def get(self) -> jsonify:
        """
        一些固定搜索哦
        :return:
        """
        parse = MyParse()
        parse.add(name="opt",
                  choices=['all', 'unClose', 'createByMe', 'assignedToMe', 'resolvedByMe'],
                  location="args",
                  required=True)

        infos = [{
            "bugID": bug.id,
            "createTime": bug.create_time,
            "title": bug.title,
            "level": bug.level,
            "priority": bug.priority,
            "status": bug.status,
            "confirmed": bug.confirmed,
            "creater": bug.creater,
            "updater": bug.updater,
            "solutionID": bug.solution
        } for bug in Bugs.optGetBugInfos(parse.parse_args().get("opt"))]
        return jsonify(myResponse(0, infos, 'ok'))


class GroupSearch(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        from COMMENT.sqlOpt import SqlOpt
        """
           按组搜索
           group：[{"key":"","val":"","condition":"<|>|=|like||!=","opt":"and|or"}]
           :return:
       """
        parse = MyParse()
        parse.add(name="group", required=True, type=list)
        bugInfos = [{
            "bugID": info[0],
            "createTime": info[1],
            "title": info[3],
            "level": info[4],
            "priority": info[5],
            "status": info[6],
            "confirmed": info[7],
            "creater": info[8],
            "updater": info[1],
            "solutionID": info[14]
        } for info in SqlOpt("bugs").select(parse.parse_args().get("group"))]

        return jsonify(myResponse(0, bugInfos, 'ok'))


class Files(Resource):

    @auth.login_required
    def post(self, bugID):
        from werkzeug.utils import secure_filename
        from faker import Faker
        f = Faker()
        file = request.files.get('file')

        if not file:
            return jsonify(myResponse(ERROR, None, NO_FIlE))
        if not bugID:
            return jsonify(myResponse(ERROR, None, cantEmpty("bugID")))
        Bugs.get(bugID, 'bugID')

        fileName = secure_filename(file.filename)
        filePath = getFilePath(f.pystr() + '_' + fileName)

        bf = BugFile(fileName=fileName, filePath=filePath, bugID=bugID)

        try:
            file.save(filePath)
            bf.save()
            return jsonify(myResponse(SUCCESS, bf.id, OK))
        except Exception as e:
            log.error(e)
            return jsonify(myResponse(ERROR, None, SOME_ERROR_TRY_AGAIN))


@myBug.route("/getFile", methods=["GET"])
@auth.login_required
def getfile() -> jsonify:
    from flask import send_file
    parse = MyParse()
    parse.add(name="fileID", required=True, location="args")
    fileID = parse.parse_args().get("fileID")
    file = BugFile.get(fileID, "fileID")
    return send_file(file.filePath)


@myBug.route("/delFile", methods=['POST'])
@auth.login_required
def delFile() -> jsonify:
    parse = MyParse()
    parse.add(name="fileID", required=True, type=int)
    fileID = parse.parse_args().get("fileID")
    bug = BugFile.get(fileID, "fileID")
    filePath = bug.filePath
    import os
    os.remove(filePath)
    bug.delete()
    return jsonify(myResponse(SUCCESS, None, OK))


@myBug.route("/putFileName", methods=["POST"])
@auth.login_required
def putFile() -> jsonify:
    parse = MyParse()
    parse.add(name="fileID", required=True, type=int)
    parse.add(name="fileName", required=True)
    fileID = parse.parse_args().get("fileID")
    fileNewName = parse.parse_args().get('fileName')  # 没有后缀
    file = BugFile.get(fileID, "fileID")
    fileOldName = file.fileName
    fileOldPath = file.filePath
    import os
    try:
        fileNewName = fileNewName + "." + fileOldName.split(".")[1]
        fileNewPath = fileOldPath.replace(fileOldName, fileNewName)
        file.fileName = fileNewName
        file.filePath = fileNewPath
        os.rename(fileOldPath, fileNewPath)
        return jsonify(myResponse(SUCCESS, file.id, OK))
    except Exception as e:
        log.error(e)
        return jsonify(myResponse(ERROR, None, e))


api_script = Api(myBug)
api_script.add_resource(MyBugs, "/bugOpt")
api_script.add_resource(BugLists, "/getBugs")
api_script.add_resource(MyBug, "/getBug")
api_script.add_resource(Confirmed, "/confirmedBug")
api_script.add_resource(CloseBug, "/closeBug")
api_script.add_resource(CopyBug, '/copyBug')
api_script.add_resource(SearchBug, "/searchBug")
api_script.add_resource(GroupSearch, "/groupSearch")
api_script.add_resource(Files, "/uploadFiled/<path:bugID>")
