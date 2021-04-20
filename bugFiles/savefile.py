# -*- coding: utf-8 -*-

# @Time    : 2021/3/26 上午10:26
# @Author  : cyq
# @File    : savefile.py


import os
import time


def get_cwd():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bugFiles')
    return path


def getFilePath(file: str) -> str:
    filePath = get_cwd()

    # 获取本地时间，转为年-月-日格式
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 日期文件夹路径
    date_file_path = os.path.join(filePath, local_date)
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(date_file_path):
        os.makedirs(date_file_path)
    return os.path.join(os.path.join(filePath, date_file_path), file)


if __name__ == '__main__':
    a = getFilePath("fsd")
    print(a)
