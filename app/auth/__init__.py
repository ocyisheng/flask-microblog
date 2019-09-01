#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 2:09 AM
# @Author  : Gao
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes