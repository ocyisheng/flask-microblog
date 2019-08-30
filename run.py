#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:06
# @Author  : 高春阳
# @File    : run.py
# @Software: PyCharm

from app import app
from app import command

def get_local_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	ip = s.getsockname()[0]
	s.close()
	return ip


if __name__ == '__main__':
	# app.run(host=get_local_ip(), port=5000)
	# 导入自定义命令行
	command.custom_command_init()
	from werkzeug.middleware.proxy_fix import ProxyFix

	app.wsgi_app = ProxyFix(app.wsgi_app)
	app.run()
