#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 16:56
# @Author  : 高春阳
# @File    : config.py
# @Software: PyCharm


import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# 加载.env 配置文件
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
	# 激活跨站点请求伪造保护
	CSRF_ENABLED = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'

	# SQLAlchemy orm设置
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# 分页配置
	POSTS_PER_PAGE = 5
	# 语言本地化
	LANGUAGES = ['en', 'zh']

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT') or 25
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	# 重要，QQ邮箱需要使用SSL。True
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['your-email@example.com']
