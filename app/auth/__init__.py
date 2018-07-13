#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Blueprint

auth = Blueprint('auth', __name__)
# 在末尾导入相关模块，是为了避免循环导入依赖，因为在下面的模块中还要导入蓝本admin
from . import views

if __name__ == '__main__':
    pass
