#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional

from app import models


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                     message='用户名不能为特殊字符')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我', default=False)


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                     message='用户名不能为特殊字符')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])

    def validate_username(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        if models.User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已被注册！')


if __name__ == '__main__':
    pass
