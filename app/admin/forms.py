#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional
from flask_login import current_user
from flask_mongoengine.wtf import model_form

from app import models



class UserForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    role = SelectField('角色', choices=models.ROLES)


class SuUserForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    is_superuser = BooleanField('超级用户', default=True)
    is_email_confirmed = BooleanField('邮箱验证')
    role = SelectField('角色', choices=models.ROLES)
    display_name = StringField('显示名称', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                          message='用户名不能为特殊字符')])
    biography = StringField('个人简介')
    homepage_url = StringField('主页', validators=[URL(), Optional()])
    weibo = StringField('微博', validators=[URL(), Optional()])
    weixin = StringField('微信', validators=[Optional(), URL()])
    twitter = StringField('Twitter', validators=[URL(), Optional()])
    github = StringField('github', validators=[URL(), Optional()])
    facebook = StringField('Facebook', validators=[URL(), Optional()])
    linkedin = StringField('Linkedin', validators=[URL(), Optional()])


class ProfileForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    ddisplay_name = StringField('显示名称', validators=[DataRequired(), Length(1, 64),
                                                    Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                           message='用户名不能为特殊字符')])
    biography = StringField('个人简介')
    homepage_url = StringField('主页', validators=[URL(), Optional()])
    weibo = StringField('微博', validators=[URL(), Optional()])
    weixin = StringField('微信', validators=[Optional(), URL()])
    twitter = StringField('Twitter', validators=[URL(), Optional()])
    github = StringField('github', validators=[URL(), Optional()])
    facebook = StringField('Facebook', validators=[URL(), Optional()])
    linkedin = StringField('Linkedin', validators=[URL(), Optional()])


class PasswordForm(FlaskForm):
    current_password = PasswordField('当前密码', validators=[DataRequired()])
    new_password = PasswordField('新密码',
                                 validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('当前密码错误')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码',
                             validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
