#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Flask
from app.ext import db, principal, login_manager,bootstrap
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    principal.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/admin')

    return app


if __name__ == '__main__':
    pass
