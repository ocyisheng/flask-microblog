#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 17:01
# @Author  : 高春阳
# @File    : froms.py
# @Software: PyCharm

from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember_Me', default=False)
    submit = SubmitField('Sign In')