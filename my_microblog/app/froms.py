#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 17:01
# @Author  : 高春阳
# @File    : froms.py
# @Software: PyCharm

from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)