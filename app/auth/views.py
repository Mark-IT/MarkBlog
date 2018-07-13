#! /usr/bin/env python
# -*- coding: utf-8 -*-
# adminor:huchong
from flask import render_template, redirect, url_for, flash, request, current_app, \
    session, abort, g, make_response
from . import auth
from .forms import LoginForm, RegistrationForm, EditUserProfileForm
from app.models import User, Article
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
from app.auth.permissions import admin_permission, editor_permission, reader_permission


@auth.route('/')
def index():
    return render_template('admin/index.html', current_user=current_user, title='管理首页')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get_or_404(username=form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.username))

            if current_user.is_adminenticated:
                flash('%s login successfully.' % (current_user.username))
            next = request.args.get('next')
            return redirect(next or url_for('admin.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form, current_user=current_user, title='用户登录')


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.admin_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    flash('You have been logged out.')
    return redirect(url_for('admin.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data)
        user.password = form.password.data
        user.role = form.role.data
        user.save()
        flash('注册成功，现在可以登录了!')
    return render_template('admin/register.html', form=form, title='用户注册')


if __name__ == '__main__':
    pass
