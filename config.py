#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
import os
import sys
import hashlib


def get_env_value(key, default_value=''):
    print(sys.version_info)
    if sys.version_info < (3, 0):
        return os.environ.get(key, default_value).decode('utf8')
    else:
        return os.environ.get(key, default_value)


MarkBlogSettings = {
    'allow_registration': os.environ.get('allow_registration', 'true').lower() == 'true',
    'allow_su_creation': os.environ.get('allow_su_creation', 'true').lower() == 'true',
    'pagination': {
        'per_page': int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
        'archive_per_page': int(os.environ.get('archive_per_page', 20)),
    },
    'blog_meta': {
        'name': get_env_value('name', 'Mini Blog'),
        'subtitle': get_env_value('subtitle', '爱技术、爱生活'),
        'description': get_env_value('description', '爱技术、爱生活'),
        'wechat_name': get_env_value('wechat_name', 'Mark Blog Wechat Root'),
        'wechat_subtitle': get_env_value('wechat_subtitle', 'Mark Blog Wechat Subtitle'),
        'owner': get_env_value('owner', 'Gevin'),
        'keywords': get_env_value('keywords', 'python,django,flask,docker,MongoDB'),
        'google_site_verification': os.environ.get('google_site_verification') or '12345678',
        'baidu_site_verification': os.environ.get('baidu_site_verification') or '87654321',
        'sogou_site_verification': os.environ.get('sogou_site_verification') or '87654321',
    },
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
