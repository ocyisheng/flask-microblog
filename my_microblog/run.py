#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:06
# @Author  : 高春阳
# @File    : run.py
# @Software: PyCharm

from app import app

if __name__ == '__main__':
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    app.run(host=ip, port='5000', debug=True)
    # app.run(host='127.0.0.1', port='5000', debug=True)
