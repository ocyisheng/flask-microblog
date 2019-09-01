#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 2:11 AM
# @Author  : Gao
# @File    : email.py
# @Software: PyCharm

from flask import render_template, current_app
from flask_babel import _
from app.email_notify import send_email


def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email(subject=_('[Microblog] Reset Your Password'),
			   sender=current_app.config['ADMINS'][0],
			   recipients=[user.email],
			   text_body=render_template('email/reset_password.txt', user=user, token=token),
			   html_boy=render_template('email/reset_password.html', user=user, token=token))
