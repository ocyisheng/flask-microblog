#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 16:22
# @Author  : 高春阳
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# 从config模块中导入Config类
from config import Config
import logging
from logging.handlers import SMTPHandler
import os
from logging.handlers import RotatingFileHandler

# flask
app = Flask(__name__)
# 配置
app.config.from_object(Config)
# db
db = SQLAlchemy(app)
# db迁移
migrate = Migrate(app, db)
# 登陆扩展
login = LoginManager(app)
# 强制登陆认证
login.login_view = 'login'
# 邮件
mail = Mail(app)
# 页面美化 框架
bootstrap = Bootstrap(app)
# 时间处理
moment = Moment(app)

from app import routes, models, errors
from app.models import User, Post


# 向flask shell运行环境中 添加自定义上下文
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


# 邮件错误通知
def mail_notify():
    if app.config['MAIL_SERVER']:
        auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                               fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                               toaddrs=app.config['ADMINS'],
                               subject='Microblog Failure',
                               credentials=auth,
                               secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


# 本地日志文件
def file_logging():
	if app.env is 'production':
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)


if not app.debug:
    mail_notify()
    file_logging()
