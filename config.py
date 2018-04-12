# coding=utf-8


import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is secret string'
    # sqlalchemy将会追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevConfig(Config):

    # 开启调试模式
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql:///example' 


# 单元测试
class TestingConfig(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql:///example' 


config = {
    'development': DevConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
