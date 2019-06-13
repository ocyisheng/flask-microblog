#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 16:56
# @Author  : 高春阳
# @File    : config.py
# @Software: PyCharm

# 激活跨站点请求伪造保护
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess!'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accoutns/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'},

]