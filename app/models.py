#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from . import db
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime


class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, primary_key=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.utcnow, required=True)
    is_email_confirmed = db.BooleanField(default=False)
    role = db.BooleanField(default=False)
    status = db.BooleanField(default=False)

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


class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False


Article_TYPES = ((0, 'draft'), (1, 'published'))


class Article(db.Document):  # 文章
    meta = {
        'allow_inheritance': True,  # 运行被继承
        'ordering': ['-pub_time']
    }
    title = db.StringField(required=True, max_length=255)
    content = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(max_length=64)
    tags = db.ListField(db.StringField(max_length=32))
    body = db.StringField()
    body_html = db.StringField()
    body_toc = db.StringField()
    status = db.IntField(required=True, choices=Article_TYPES)
    pub_time = db.DateTimeField(default=datetime.utcnow)
    update_time = db.DateTimeField(default=datetime.utcnow)

    def __unicode__(self):
        return self.title


if __name__ == '__main__':
    pass
