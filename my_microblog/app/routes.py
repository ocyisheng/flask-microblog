#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:09
# @Author  : 高春阳
# @File    : routes.py
# @Software: PyCharm

from app import app
from app import db
from .froms import LoginForm, RegistrationForm, EditProfileForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime


# 在请求发出前，记录当前用户访问的时间，作为上次访问的时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
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
                           posts=posts)


# 关注
@app.route('/user/<username>/follow')
@login_required
def follow(username):
    followed_user = User.query.filter_by(username=username).first_or_404()
    current_user.follow(followed_user)
    posts = [
        {'author': followed_user, 'body': 'Test post #1'},
        {'author': followed_user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=followed_user, posts=posts)


# 取消关注
@app.route('/user/<username>/unfollow')
@login_required
def unfollow(username):
    followed_user = User.query.filter_by(username=username).first_or_404()
    current_user.unfollow(followed_user)
    posts = [
        {'author': followed_user, 'body': 'Test post #1'},
        {'author': followed_user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=followed_user, posts=posts)


# 用户信息展示
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations , you are now a registered user !')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# 登陆
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
        # 登陆UserMinx，记录登陆信息
        login_user(user=user, remember=form.remember_me.data)
        # 重定向到next 页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).decode_netloc() != '':
            next_page = url_parse('index')
        flash('Login successful')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
