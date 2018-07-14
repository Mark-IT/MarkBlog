#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional
from app.models import ROLES, User,POST_STATUS


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 64),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                     message='用户名不能为特殊字符')])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 10)])
    remember_me = BooleanField(label='保持登录', default=False)
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 64),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                     message='用户名不能为特殊字符')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    role = SelectField('角色权限', choices=ROLES)
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        if User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已被注册！')


class EditUserProfileForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    username = StringField('显示名称', validators=[DataRequired(), Length(4, 64),
                                               Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0,
                                                      message='用户名不能为特殊字符')])

    about_me = StringField('介绍', validators=[Length(0, 256)])
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                        User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已经被使用！')

    def validate_username(self, field):
        if field.data != self.user.username and \
                        User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已经被使用！')


if __name__ == '__main__':
    pass
