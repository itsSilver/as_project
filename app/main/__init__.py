# coding=utf-8

from flask import Blueprint

# 实例化Blueprint类,管理路由
main = Blueprint('main', __name__)

from . import index, errors
