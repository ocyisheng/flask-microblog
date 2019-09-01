#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 2:43 AM
# @Author  : Gao
# @File    : routes.py
# @Software: PyCharm

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
from app.translate import translate
from app.main import bp


# 在请求发出前，记录当前用户访问的时间，作为上次访问的时间
@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	# g.locale = str(get_locale())
	# 注意flask_babel.get_locale返回的和g.locale 需要的不相同
	g.locale = 'zh_CN' if str(get_locale()).startswith('zh') else str(get_locale())


# 翻译
@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
	result_data = {'text': translate(request.form['text'], request.form['source_lang'], request.form['dest_lang'])}
	return jsonify(result_data)


# 首页
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		language = guess_language(form.post.data)
		if language == 'UNKONWN' or len(language) > 5:
			language = ''
		post = Post(body=form.post.data, author=current_user, language=language)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live !'))
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int)
	# posts = current_user.followed_posts().all()
	# 分页
	posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	# url_for 可以将任何未使用参数包含到url中
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template("index.html",
						   title=_('Home Page'),
						   form=form,
						   posts=posts.items,
						   next_url=next_url,
						   prev_url=prev_url)


# 浏览全部帖子
@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
	# posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',
						   title=_('Explore'),
						   posts=posts.items,
						   next_url=next_url,
						   prev_url=prev_url)


# 用户信息展示
@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	# posts = Post.query.filter_by(author=user).all()
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	prev_url = url_for('main.user', username=username, page=posts.prev_num) if posts.has_prev else None
	next_url = url_for('main.user', username=username, page=posts.next_num) if posts.has_next else None

	return render_template('user.html',
						   title=_('Profile'),
						   user=user,
						   posts=posts.items,
						   next_url=next_url,
						   prev_url=prev_url)


# 编辑个人信息
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


# 关注
@bp.route('/follow/<username>')
@login_required
def follow(username):
	followed_user = User.query.filter_by(username=username).first()
	if not followed_user:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('main.index'))
	if followed_user == current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.follow(followed_user)
	db.session.commit()
	flash(_('You are following %(username)s !', username=username))
	return redirect(url_for('main.user', username=username))


# 取消关注
@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	followed_user = User.query.filter_by(username=username).first()
	if not followed_user:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('main.index'))
	if followed_user == current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(followed_user)
	db.session.commit()
	flash(_('You are unfollowing %(username)s !', username=username))
	return redirect(url_for('main.user', username=username))


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user_popup.html', user=user)
