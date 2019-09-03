#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:06
# @Author  : 高春阳
# @File    : run.py
# @Software: PyCharm

from app import create_app, db, cli
from app.models import User, Post, Notification, Message

# def get_local_ip():
# 	import socket
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	s.connect(('8.8.8.8', 80))
# 	ip = s.getsockname()[0]
# 	s.close()
# 	return ip

# 主入口程序，生成app
app = create_app()
# 向app注册cli 自定义命令行
cli.register(app)


# 向flask shell运行环境中 添加自定义上下文
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post, 'Notification': Notification, 'Message': Message}


if __name__ == '__main__':
	# app.run(host=get_local_ip(), port=5000)
	# 导入自定义命令行
	from werkzeug.middleware.proxy_fix import ProxyFix

	app.wsgi_app = ProxyFix(app.wsgi_app)
	app.run()
