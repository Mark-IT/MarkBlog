#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from . import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime

ROLES = (('admin', 'admin'),
         ('editor', 'editor'),
         ('writer', 'writer'),
         ('reader', 'reader'))
SOCIAL_NETWORKS = {
    'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
    'weixin': {'fa_icon': 'fa fa-weixin', 'url': None},
    'twitter': {'fa_icon': 'fa fa fa-twitter', 'url': None},
    'github': {'fa_icon': 'fa fa-github', 'url': None},
    'facebook': {'fa_icon': 'fa fa-facebook', 'url': None},
    'linkedin': {'fa_icon': 'fa fa-linkedin', 'url': None},
}


class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, primary_key=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.utcnow, required=True)
    is_email_confirmed = db.BooleanField(default=False)
    is_superuser = db.BooleanField(default=False)
    role = db.StringField(max_length=32, default='reader', choices=ROLES)
    display_name = db.StringField(max_length=255, default=username)
    biography = db.StringField()
    social_networks = db.DictField(default=SOCIAL_NETWORKS)
    homepage_url = db.URLField()

    @property
    def password(self):
        raise AttributeError('非明文密码，不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'confirm': self.username})

    def confirm_email(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            print('access token expired! ')
            return False
        except BadSignature:
            print('access token Bad!')
            return False
        if data.get('confirm') != self.username:
            return False
        self.is_email_confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'reset': self.username})

    @staticmethod
    def reset_password(token, new_password):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            print('access token expired! ')
            return False
        except BadSignature:
            print('access token Bad!')
            return False

        try:
            user = User.objects.get(username=data.get('reset'))
        except Exception:
            return False

        user.password = new_password
        user.save()
        return True

    def get_id(self):
        try:
            # return unicode(self.username)
            return self.username

        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def is_admin(self):
        return self.role

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def is_author(self):
        return Article.query.filter_by(author_id=self.id).first()

    def __unicode__(self):
        return self.username


class Post(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)  # 别名
    fix_slug = db.StringField(max_length=255, required=False)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(max_length=64)
    tags = db.ListField(db.StringField(max_length=30))
    is_draft = db.BooleanField(default=False)
    post_type = db.StringField(max_length=64, default='post')
    weight = db.IntField(default=10)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-pub_time']
    }


class Draft(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(max_length=64, default='default')
    tags = db.ListField(db.StringField(max_length=30))
    is_draft = db.BooleanField(default=True)
    post_type = db.StringField(max_length=64, default='post')
    weight = db.IntField(default=10)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-update_time']
    }


class Tracker(db.Document):
    post = db.ReferenceField(Post)
    ip = db.StringField()
    user_agent = db.StringField()
    create_time = db.DateTimeField()

    def __unicode__(self):
        return self.ip

    meta = {
        'allow_inheritance': True,
        'indexes': ['ip'],
        'ordering': ['-create_time']
    }


if __name__ == '__main__':
    pass
