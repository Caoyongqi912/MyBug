# -*- coding: utf-8 -*-

# @Time    : 2021/2/5 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import requests
import random
from faker import Faker

f = Faker()


class MyRequest:
    Host = "http://127.0.0.1:5000/"

    def __init__(self):
        pass

    def go(self, method, url, params=None, body=None, auth=None):

        if method == "GET":
            pass

        elif method == "POST":
            resp = requests.post(url=self.Host + url, params=params, json=body, auth=auth)
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
            "projectId": 11,
            "productId": 9,
            "platformId": random.randint(11, 15),
            "buildId": random.randint(11, 20),
            "title": f.sentence(),
            'assignedTo': random.randint(1, 11),
            "mailTo": random.randint(1, 11),
            "stepsBody": f.text()
        }
        rep = self.go(method="POST",url="api/bugOpt",body=body,auth=('cyq','cyq'))
        print(rep.json())



if __name__ == '__main__':
    m = MyRequest()
    m.add_bug()
