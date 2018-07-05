#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import abort, redirect, url_for, render_template, request, current_app, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_principal import Identity, AnonymousIdentity, identity_changed
from app import models
from app.auth import forms
from app.auth.permissions import editor_permission
from config import MarkBlogSettings

POST_TYPES = models.POST_TYPE_CHOICES
# POST_TYPES = MiniBlogSettings['post_types']
PER_PAGE = MarkBlogSettings['pagination'].get('admin_per_page', 10)

article_models = {
    'post': models.Post,
    'draft': models.Draft
}


def get_current_user():
    user = models.User.objects.get(username=current_user.get_id())
    return user


def register(create_su=False):
    if not MarkBlogSettings['allow_registration']:
        msg = '禁止注册，请联系管理员'
        abort(403, msg)

    if create_su and not MarkBlogSettings['allow_su_creation']:
        msg = '禁止注册超级用户，请联系管理员'
        abort(403, msg)

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data

        user.display_name = user.username

        if create_su and MarkBlogSettings['allow_su_creation']:
            user.is_superuser = True
        user.save()

        return redirect(url_for('main.index'))

    return render_template('accounts/registration.html', form=form)


def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.objects.get(username=form.username.data)
        except models.User.DoesNotExist:
            user = None

        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.last_login = datetime.now
            user.save()
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
            return redirect(request.args.get('next') or url_for('admin.index'))

        flash('无效的用户名或密码', 'danger')

    return render_template('accounts/login.html', form=form)


@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    flash('注销成功', 'success')
    return redirect(url_for('accounts.login'))


if __name__ == '__main__':
    pass
