#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:09
# @Author  : 高春阳
# @File    : views.py
# @Software: PyCharm

from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland !'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool ！'
        },
    ]
    return render_template("index.html",
                           user=user,
                           posts=posts)

