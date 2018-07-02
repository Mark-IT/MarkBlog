#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from config import config

db = MongoEngine()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)
    moment.init_app(app=app)
    login_manager.init_app(app)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app


if __name__ == '__main__':
    pass
