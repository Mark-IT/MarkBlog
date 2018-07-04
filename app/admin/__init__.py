#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Blueprint
from app.admin import views

admin = Blueprint('admin', __name__, template_folder="templates", static_url_path='', static_folder='static')
admin.add_url_rule('/posts/', view_func=views.PostsList.as_view('posts'))
admin.add_url_rule('/pages/', view_func=views.PostsList.as_view('pages'), defaults={'post_type': 'page'})

accounts = Blueprint('accounts', __name__)
# accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/registration/', 'register', views.register, methods=['GET', 'POST'])
accounts.add_url_rule('/registration/su', 'register_su', views.register, defaults={'create_su': True},
                      methods=['GET', 'POST'])

if __name__ == '__main__':
    pass
