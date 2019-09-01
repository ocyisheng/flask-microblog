#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 3:02 PM
# @Author  : Gao
# @File    : email_notify.py
# @Software: PyCharm

from flask import current_app
from threading import Thread
from flask_mail import Message
from app import mail

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
	Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


