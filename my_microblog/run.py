#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:06
# @Author  : 高春阳
# @File    : run.py
# @Software: PyCharm

from app import app

if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.0.137', port='5000')
