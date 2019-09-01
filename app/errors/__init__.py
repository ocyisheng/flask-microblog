#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 1:55 AM
# @Author  : Gao
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers