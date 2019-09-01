#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 2:11 AM
# @Author  : Gao
# @File    : routes.py
# @Software: PyCharm

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


# 登陆
@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('Invalid username or password'))
			return redirect(url_for('auth.login'))
		# 登陆UserMinx，记录登陆信息
		login_user(user=user, remember=form.remember_me.data)
		# 重定向到next 页面
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).decode_netloc() != '':
			next_page = url_for('main.index')
			flash(_('Login successful'))
		return redirect(next_page)
	return render_template('auth/login.html', title=_('Sign In'), form=form)


# 登出
@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))


# 注册
@bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('Congratulations , you are now a registered user !'))
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title=_('Register'), form=form)


# 请求重置密码
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	# 若已经登录,不需要重置
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(_('Chceck your email for the instructions to reset your password !'))
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', title=_('Reset Password'), form=form)


# 重置密码
@bp.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	# 验证token是否通过
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_('Your password has been reset.'))
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', title=_('Reset Password'), form=form)
