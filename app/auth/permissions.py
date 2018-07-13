#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask_principal import  Permission, RoleNeed, UserNeed, identity_loaded
from flask_login import current_user

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor')).union(admin_permission)
reader_permission = Permission(RoleNeed('reader')).union(editor_permission)


# 用法：
# # protect a view with a principal for that need
# @app.route('/admin')
# @admin_permission.require()
# def do_admin_index():
#     return Response('Only if you are an admin')

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

    identity.allow_read = identity.can(reader_permission)
    identity.allow_edit = editor_permission.allows(identity)
    identity.allow_admin = admin_permission.allows(identity)


if __name__ == '__main__':
    pass
