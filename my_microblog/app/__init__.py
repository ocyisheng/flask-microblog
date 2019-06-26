#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 16:22
# @Author  : 高春阳
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# 从config模块中导入Config类
from config import Config

# flask
app = Flask(__name__)
# 配置
app.config.from_object(Config)
# db
db = SQLAlchemy(app)
# db迁移
migrate = Migrate(app, db)
# 登陆扩展
login = LoginManager(app)


from app import routes, models
from app.models import User, Post

# 向flask shell运行环境中 添加自定义上下文
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}
