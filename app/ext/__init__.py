# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_login import LoginManager
from flask_principal import Principal

db = MongoEngine()
admin = Admin()
principal = Principal()
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 安全等级
login_manager.login_view = 'auth.login'  # 登录页面的端点


def main():
    pass


if __name__ == '__main__':
    main()
