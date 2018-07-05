#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import request, render_template
from mongoengine.queryset.visitor import Q
from app import models
from config import MarkBlogSettings

PER_PAGE = MarkBlogSettings['pagination'].get('per_page', 10)
ARCHIVE_PER_PAGE = MarkBlogSettings['pagination'].get('archive_per_page', 10)
BACKGROUND = MarkBlogSettings['background_image']
# DAOVOICE = MarkBlogSettings['daovoice']


def get_base_data():
    pages = models.Post.objects.filter(post_type='page', is_draft=False)
    blog_meta = MiniBlogSettings['blog_meta']
    data = {
        'blog_meta': blog_meta,
        'pages': pages,
        'bg_home': BACKGROUND['home'],
        'bg_post': BACKGROUND['post'],
        'bg_about': BACKGROUND['about'],
        # 'qiniu': BACKGROUND['qiniu'],
        'allow_daovoice': DAOVOICE['allow_daovoice'],
        'dao_app_id': DAOVOICE['app_id'],
    }
    return data


def list_posts():
    posts = models.Post.objects.filter(post_type='post', is_draft=False).order_by('-weight', '-pub_time')
    posts = posts.filter(Q(weight__gt=0) | Q(weight=None))

    tags = posts.distinct('tags')

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1

    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')
    keywords = request.args.get('keywords')

    if keywords:
        # posts = posts.filter(raw__contains=keywords )
        posts = posts.filter(Q(raw__icontains=keywords) | Q(title__icontains=keywords))

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)

    # group by aggregate
    category_cursor = models.Post._get_collection().aggregate([
        {'$group':
             {'_id': {'category': '$category'},
              'name': {'$first': '$category'},
              'count': {'$sum': 1},
              }
         }
    ])

    widgets = models.Widget.objects(allow_post_types='post')

    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    data = get_base_data()
    data['posts'] = posts
    data['cur_category'] = cur_category
    data['category_cursor'] = category_cursor
    data['cur_tag'] = cur_tag
    data['tags'] = tags
    data['keywords'] = keywords
    data['widgets'] = widgets

    return render_template('blog/index.html', **data)


if __name__ == '__main__':
    pass
