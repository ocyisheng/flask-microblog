#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:09
# @Author  : 高春阳
# @File    : routes.py
# @Software: PyCharm

from app import app
from .froms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user=user, remember=form.remember_me.data)
        flash('Login successful')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))