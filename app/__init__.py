#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Flask
from app.ext import db, admin, principal, login_manager
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)
    admin.init_app(app)
    principal.init_app(app)
    login_manager.init_app(app)

    return app


if __name__ == '__main__':
    pass
