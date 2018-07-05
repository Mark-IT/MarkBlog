#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Blueprint
from . import views
blog = Blueprint('blog', __name__)
main.add_url_rule('/', 'index', views.list_posts)
if __name__ == '__main__':
    pass
