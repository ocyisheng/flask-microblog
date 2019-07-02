#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 16:56
# @Author  : 高春阳
# @File    : config.py
# @Software: PyCharm


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# 激活跨站点请求伪造保护
	CSRF_ENABLED = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'

	# SQLAlchemy orm设置
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# # 激活跨站点请求伪造保护
	# CSRF_ENABLED = True
	# SECRET_KEY = 'you-will-never-guess!'
	#
	# OPENID_PROVIDERS = [
	# 	{'name': 'Google', 'url': 'https://www.google.com/accoutns/o8/id'},
	# 	{'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
	# 	{'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
	# 	{'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
	# 	{'name': 'MyOpenID', 'url': 'https://www.myopenid.com'},
	#
	# ]
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['your-email@example.com']
