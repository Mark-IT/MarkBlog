#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
import os
import hashlib

MarkBlogSettings = {
    'allow_registration': os.environ.get('allow_registration', 'true').lower() == 'true',
    'allow_su_creation': os.environ.get('allow_su_creation', 'true').lower() == 'true',
    'pagination': {
        'per_page': int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
        'archive_per_page': int(os.environ.get('archive_per_page', 20)),
    }
}


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or hashlib.new(name='md5', string='o12fasgk@#').hexdigest()
    MONGODB_SETTINGS = {'DB': 'MarkBlog'}

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME') or 'MarkBlog',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
        'port': 27017,
        'username': 'admin',
        'password': 'admin123'
    }


class PrdConfig(Config):
    # DEBUG = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME') or 'test',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
        'port': 27017
    }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    WTF_CSRF_ENABLED = False
    MONGODB_SETTINGS = {
        'db': 'MarkBlog Test',
        'is_mock': True
    }


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
if __name__ == '__main__':
    pass
