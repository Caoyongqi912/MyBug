# -*- coding: utf-8 -*-

# @Time    : 2021/2/3 下午3:23
# @Author  : cyq
# @File    : init_data.py


import random
from faker import Faker
from APP import create_app
from Model.models import *

f = Faker(locale="zh_CN")


def add_user(nums: int):
    create_app().app_context().push()

    for i in range(nums):
        User(account=f.name(), name=f.name(), password=f.password(), admin=False, department=random.randint(1, 10),
             gender=random.choice([1, 0])).save()

    print("ok")


def add_project(nums: int):
    create_app().app_context().push()

    for i in range(nums):
        Project(name=f.company()).save()
    print("ok")


def add_department(nums: int):
    create_app().app_context().push()

    for i in range(nums):
        Department(name=f.job()).save()
    print("ok")


def add_product(nums: int):
    create_app().app_context().push()
    for i in range(nums):
        Product(name=f.word(), projectId=random.randint(1, 10)).save()
    print("ok")


def add_solution(nums: int):
    create_app().app_context().push()
    s = ['设计如此', '重复缺陷', '不予解决', '无法重现', '已解决', '信息不足', '设计如此', '其他']
    for i in range(nums):
        Solution(name=random.choice(s), productId=random.randint(1, 8)).save()
    print('ok')


def add_platform(nums: int):
    create_app().app_context().push()
    p = ['Ios', "Andriod", "Windows", "Web", "Mac"]
    for i in range(nums):
        Platform(name=random.choice(p), productId=random.randint(1, 5)).save()
    print("ok")


def add_version(nums: int):
    create_app().app_context().push()
    for i in range(nums):
        Build(name=f.ipv4(), productId=random.randint(1, 10)).save()

    print("ok")


def add_error(nums: int):
    create_app().app_context().push()
    es = ['功能问题', "性能问题", "界面问题", "设计问题", "其他"]
    for i in range(nums):
        ErrorType(name=random.choice(es), productId=random.randint(1, 8)).save()

    print("ok")


if __name__ == '__main__':
    add_error(10)
