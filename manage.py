#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
import os
from app import create_app
from flask_script import Manager, Server

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=5000)
                    )

if __name__ == '__main__':
    manager.run()
