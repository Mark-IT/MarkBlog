#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional
from flask_login import current_user
from flask_mongoengine.wtf import model_form

from app import models


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我', default=False)
    submit = SubmitField('登 录')


class AddAdminForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 16, message='用户名长度要在1和16之间'),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0, message='用户名不能为特殊字符')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('重输密码', validators=[DataRequired()])
    submit = SubmitField('注 册')

    def validate_username(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        if models.User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已被注册！')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('重输密码', validators=[DataRequired()])
    submit = SubmitField('更新密码')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('当前密码错误')


class AddUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64, message='姓名长度要在1和64之间'),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0, message='用户名不能为特殊字符')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    role = SelectField('权限', choices=[('True', '管理员'), ('False', '一般用户')])
    status = SelectField('状态', choices=[('True', '正常'), ('False', '注销')])
    submit = SubmitField('添加用户')

    def validate_username(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('邮箱已被注册！')


class EditUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64, message='姓名长度要在1和64之间'),
                                              Regexp('^[\u4E00-\u9FFF A-Za-z0-9_.]+$', flags=0, message='用户名不能为特殊字符')])
    email = StringField('邮箱', validators=[DataRequired(), Length(6, 64, message='邮件长度要在6和64之间'),
                                          Email(message='邮件格式不正确！')])
    role = SelectField('权限', choices=[('True', '管理员'), ('False', '一般用户')])
    status = SelectField('状态', choices=[('True', '正常'), ('False', '注销')])
    submit = SubmitField('修改用户')


class DeleteUserForm(FlaskForm):
    user_id = StringField()


class WriteArticleForm(FlaskForm):
    title = StringField('标题')
    body = TextAreaField('文章内容')
    category = StringField('分类')
    tags = StringField('标签')
    submit = SubmitField('提交')


class EditArticleForm(FlaskForm):
    title = StringField('标题')
    body = TextAreaField('文章内容')
    category_name = StringField('分类')
    tags_name = StringField('标签')
    submit = SubmitField('提交')


class DeleteArticleForm(FlaskForm):
    article_id = StringField()


class BaidutongjiForm(FlaskForm):
    token = StringField('键值')
    status = SelectField('状态', choices=[('True', '启用'), ('False', '停用')])
    submit = SubmitField('提交')


class AddFolderForm(FlaskForm):
    directory = StringField('文件夹')
    submit = SubmitField('确定')
