#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 16:22
# @Author  : 高春阳
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# 从config模块中导入Config类
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import views, models

# 向flask shell运行环境中 添加自定义上下文
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User':models.User, 'Post':models.Post }
