#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Flask
from flask_mongoengine import MongoEngine
from config import config

db = MongoEngine()



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)

    return app


if __name__ == '__main__':
    pass
