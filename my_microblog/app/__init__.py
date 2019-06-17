#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 16:22
# @Author  : 高春阳
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from app import views, models