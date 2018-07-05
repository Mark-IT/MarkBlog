#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Blueprint
from app.auth import views
accounts = Blueprint('accounts', __name__)
# accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/registration/', 'register', views.register, methods=['GET', 'POST'])
accounts.add_url_rule('/registration/su', 'register_su', views.register, defaults={'create_su': True},
                      methods=['GET', 'POST'])
accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/logout/', 'logout', views.logout)
if __name__ == '__main__':
    pass

