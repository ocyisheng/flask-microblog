#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 3:02 PM
# @Author  : Gao
# @File    : email.py
# @Software: PyCharm

from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread
from flask_babel import _

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_boy):
	msg = Message(subject=subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_boy
	# 同步发送
	# mail.send(msg)
	# 异步线程发送
	Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email(subject=_('[Microblog] Reset Your Password'),
			   sender=app.config['ADMINS'][0],
			   recipients=[user.email],
			   text_body=render_template('email/reset_password.txt', user=user, token=token),
			   html_boy=render_template('email/reset_password.html', user=user, token=token))
