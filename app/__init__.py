#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 16:22
# @Author  : 高春阳
# @File    : __init__.py
# @Software: PyCharm

from flask import Flask, request,current_app
# 从config模块中导入Config类
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

## 扩展对象生成
# db
db = SQLAlchemy()
# db迁移
migrate = Migrate()
# 登陆扩展
login = LoginManager()
# 强制登陆认证
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
# 邮件
mail = Mail()
# 页面美化 框架
bootstrap = Bootstrap()
# 时间处理
moment = Moment()
# 语言本地话
babel = Babel()


def create_app(config_class=Config):
	# app对象
	app = Flask(__name__)
	# 向app中添加配置
	app.config.from_object(config_class)

	# 向app中添加相应扩展
	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	babel.init_app(app)

	## 向app中注册各个子模块的蓝图
	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	# 添加前置路由作为命名空间 /autho/login ...
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	# 错误邮件通知与错误本地记录
	if not app.debug and not app.testing:
		mail_notify(app)
		file_logging(app)

	return app


# 语言本地化 在request前 利用装饰器 获取最适合的语言版本
@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(current_app.config['LANGUAGES'])


# 邮件错误通知
def mail_notify(app):
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
def file_logging(app):
	if app.env is 'production':
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(
			logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Microblog startup')
