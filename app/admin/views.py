#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import abort, redirect, url_for, render_template, request
from flask.views import MethodView
from flask_login import current_user

from app import models
from app.admin import forms
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


class PostsList(MethodView):
    template_name = 'admin/posts.html'
    is_draft = False
    article_model = models.Post

    def get(self, post_type='post'):
        posts = self.article_model.objects.filter(post_type=post_type).order_by('-update_time', '-weight')

        if not g.identity.can(editor_permission):
            posts = posts.filter(author=get_current_user())

        try:
            cur_page = int(request.args.get('page', 1))
        except:
            cur_page = 1

        posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

        return render_template(self.template_name, posts=posts, post_type=post_type, is_draft=self.is_draft)


if __name__ == '__main__':
    pass
