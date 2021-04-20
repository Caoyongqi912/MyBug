# -*- coding: utf-8 -*-

# @Time    : 2021/2/5 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import requests
import random
from faker import Faker
import os

f = Faker()


class MyRequest:
    Host = "http://127.0.0.1:5000/"

    def __init__(self):
        pass

    def go(self, method, url, params=None, body=None, files=None, auth=("cyq", "cyq")):

        if method == "GET":
            return requests.get(url=self.Host + url, params=params, json=body, auth=auth)

        elif method == "POST":
            resp = requests.post(url=self.Host + url, params=params, json=body, auth=auth, files=files)
            return resp

        elif method == "PUT":
            resp = requests.put(url=self.Host + url, params=params, json=body, auth=auth)
            return resp
        else:
            resp = requests.delete(url=self.Host + url, params=params, json=body, auth=auth)
            return resp

    def add_solution(self, name, productId):
        body = {
            "name": name,
            "productId": productId
        }
        rep = self.go(method="POST", url="api/solutionOpt", body=body, auth=('cyq', "cyq"))
        print(rep.json())

    def del_solution(self, id, pid):
        body = {
            "id": id,
            "productId": pid
        }
        rep = self.go(method="DELETE", url="api/solutionOpt", body=body, auth=('cyq', "cyq"))
        print(rep.json())

    def put_solution(self, name, productId):
        body = {
            "name": name,
            "productId": productId
        }
        rep = self.go(method="PUT", url="api/solutionOpt", body=body, auth=('cyq', "cyq"))
        print(rep)

    def add_bug(self):
        body = {
            "projectId": 1,
            "productId": 1,
            "platformId": 1,
            "buildId": 1,
            "title": f.sentence(),
            'assignedTo': 1,
            "mailTo": 1,
            "stepsBody": f.text(),
            "level": "p1",
            "priority": random.choice(['p1', 'p2', 'p3', 'p4']),

        }
        testpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/test.txt"
        file = {"file": open(testpath, "rb")}
        rep = self.go(method="POST", url="api/bugOpt", body=body, auth=('cyq', 'cyq'))
        print(rep.json())

    def test(self):
        body = {"name": "cyq", "age": "111", "cname": "hahha"}
        rep = self.go(method="POST", url="api/test", body=body)
        print(rep.json())

    def getOneBug(self):
        params = {"bugID": 1}
        json = {'name': 'cyq'}
        rep = self.go(method="GET", url="api/closeBug", params=params, body=json, auth=('cyq', 'cyq'))

        print(rep.json())

    def upload(self):
        testpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/test.png"
        file = {"file": open(testpath, "rb")}
        rep = self.go(method="POST", url="api/uploadFiled/2", files=file, auth=('cyq', 'cyq'))
        print(rep.text)

    def search(self):
        json = {
            "opt": 1,
            "searchID": 1
        }
        rep = self.go(method="POST", url="api/search", body=json, auth=("cyq", "cyq"))
        print(rep.json())

    def removeFile(self):
        json = {
            "fileID": 4
        }
        rep = self.go(method="POST", url="api/delFile", body=json, auth=("cyq", "cyq"))
        print(rep.json())

    def putFile(self):
        json = {
            "fileID": 1,
            "fileName": "xixixiahal"
        }
        rep = self.go(method="POST", url="api/putFileName", body=json, auth=("cyq", "cyq"))
        print(rep.text)

    def groupSearch(self):
        json = {
            "group": [{"key": "id", "val": 2, "condition": "=", "opt": "or"},
                      {"key": "id", "val": 3, "condition": "=", "opt": "or"},
                      {"key": "title", "val": "004", "condition": "like", "opt": "or"}]
        }
        rep = self.go(method="POST", url="api/groupSearch", body=json, auth=("cyq", "cyq"))
        print(rep.json())

    def buglist(self):
        param = {"productID": 1}
        rep = self.go(method="GET", url="api/getBugs", params=param, auth=("cyq", "cyq"))
        print(rep.json())

    def getbug(self):
        param = {"bugID": 2}
        rep = self.go(method="GET", url="api/getBug", params=param, auth=("cyq", "cyq"))
        print(rep.json())

    def copyBug(self):
        param = {"bugID": 2}
        rep = self.go(method="POST", url="api/copyBug", body=param, auth=("cyq", "cyq"))
        print(rep.json())

    def getFile(self):
        param = {"fileID":1}
        rep = self.go(method="GET", url="api/getFile", params=param, auth=("cyq", "cyq"))
        print(rep)

if __name__ == '__main__':
    m = MyRequest()

    m.getFile()
