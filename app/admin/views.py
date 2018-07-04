#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import abort, redirect, url_for, render_template
from app.admin import forms
from config import MiniBlogSettings
from app import models


def register(create_su=False):
    if not MiniBlogSettings['allow_registration']:
        msg = '禁止注册，请联系管理员'
        abort(403, msg)

    if create_su and not MiniBlogSettings['allow_su_creation']:
        msg = '禁止注册超级用户，请联系管理员'
        abort(403, msg)

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data

        user.display_name = user.username

        if create_su and MiniBlogSettings['allow_su_creation']:
            user.is_superuser = True
        user.save()

        return redirect(url_for('main.index'))

    return render_template('accounts/registration.html', form=form)


if __name__ == '__main__':
    pass
