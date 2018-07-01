#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder="templates", static_url_path='', static_folder='static')



if __name__ == '__main__':
    pass
