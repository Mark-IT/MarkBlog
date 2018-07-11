#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime
from markdown2 import markdown
import bleach
from app import db, login_manager

POST_STATUS = (('草稿', '草稿'), ('发布', '发布'))
ROLES = (('admin', 'admin'),
         ('editor', 'editor'),
         ('reader', 'reader'))


class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, primary_key=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.utcnow, required=True)
    is_email_confirmed = db.BooleanField(default=False)
    role = db.StringField(max_length=32, default='reader', choices=ROLES)
    display_name = db.StringField(max_length=255, default=username)

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
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def __unicode__(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user


class Comment(db.EmbeddedDocument):
    pub_time = db.DateTimeField(default=datetime.now, required=True)
    content = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)


class Article(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    category = db.StringField(max_length=64)
    tags = db.ListField(db.StringField(max_length=30))
    # CASCADE (2) - Deletes the documents associated with the reference.
    author = db.ReferenceField(User, reverse_delete_rule=2)
    content = db.StringField(required=True)
    content_html = db.StringField(required=True)

    is_draft = db.BooleanField(default=False)
    pub_time = db.DateTimeField()
    modifly_time = db.DateTimeField()
    status = db.StringField(required=True, choices=POST_STATUS)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': [{'fields': ['$title', "$content"],
                     'weights': {'title': 10, 'content': 2}
                     }],
        'ordering': ['-pub_time']
    }

    def save(self, allow_set_time=False, *args, **kwargs):
        ''' 覆写Post.save()方法，保存post时生成contnet_html字段'''
        if not allow_set_time:
            now = datetime.now()
            if not self.publish_time:
                self.publish_time = now
            self.modifly_time = now

        self.content_html = markdown(self.content, extras=['code-friendly', 'fenced-code-blocks', 'tables']).encode(
            'utf-8')
        self.content_html = get_clean_html_content(self.content_html)
        return super(Article, self).save(*args, **kwargs)


class Tracker(db.Document):
    post = db.ReferenceField(Article)
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


class ArticleStatistics(db.Document):
    post = db.ReferenceField(Article)
    visit_count = db.IntField(default=0)
    verbose_count_base = db.IntField(default=0)


def get_clean_html_content(html_content):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'hr', 'img',
                    'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'sup', 'sub']

    allowed_attrs = {
        '*': ['class'],
        'a': ['href', 'rel', 'name'],
        'img': ['alt', 'src', 'title'],
    }
    allowed_styles = ['color', 'background-color', 'font-weight', 'font-style']

    html_content = bleach.linkify(
        bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs, styles=allowed_styles, strip=True))
    return html_content


if __name__ == '__main__':
    pass
