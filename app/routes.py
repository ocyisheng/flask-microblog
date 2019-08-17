#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:09
# @Author  : 高春阳
# @File    : routes.py
# @Software: PyCharm

from app import app
from app import db
from .froms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime


# 在请求发出前，记录当前用户访问的时间，作为上次访问的时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live !')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    # posts = current_user.followed_posts().all()
    # 分页
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # url_for 可以将任何未使用参数包含到url中
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


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
    db.session.commit()
    flash('You are following {} !'.format(followed_user.username))
    return render_template('user.html', user=followed_user, posts=posts)


# 取消关注
@app.route('/user/<username>/unfollow')
@login_required
def unfollow(username):
    followed_user = User.query.filter_by(username=username).first_or_404()
    current_user.unfollow(followed_user)
    posts = Post.query.filter_by(author=followed_user).all()
    db.session.commit()
    flash('You are unfollowing {} !'.format(followed_user.username))
    return render_template('user.html', user=followed_user, posts=posts)


# 用户信息展示
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.filter_by(author=user).all()
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    prev_url = url_for('user', username=username, page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('user', username=username, page=posts.next_num) if posts.has_next else None

    return render_template('user.html', title='Profile', user=user, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


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
