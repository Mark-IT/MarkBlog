#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import render_template, request, g
from flask.views import MethodView
from flask_login import  current_user

from app import models

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

class AdminIndex(MethodView):
    # decorators = [login_required]
    template_name = 'admin/index.html'

    def get(self):
        blog_meta = MarkBlogSettings['blog_meta']
        user = get_current_user()
        return render_template(self.template_name, blog_meta=blog_meta, user=user)

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
