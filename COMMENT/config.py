# -*- coding: utf-8 -*-

# @Time    : 2021/1/4 下午2:53
# @Author  : cyq
# @File    : config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "127.0.0.1"
    redisPort = '6379'

    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    CACHE_TYPE = 'simple'
    ERROR_404_HELP = False
    CACHE_DEFAULT_TIMEOUT = 300
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    JSON_AS_ASCII = False  # 这个配置可以确保http请求返回的json数据中正常显示中文
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


    CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(Config.HOST, Config.redisPort)
    CELERY_BROKER_URL = 'redis://{}:{}'.format(Config.HOST, Config.redisPort)
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']

    # CELERYBEAT_SCHEDULE = {
    #     'import_data': {
    #         'task': 'test_ddd',
    #         'schedule': timedelta(seconds=10)
    #     },
    # }
    #

class TestingConfig(Config):
    TESTING = True
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

if __name__ == '__main__':
    print(basedir)