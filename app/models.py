#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-17 15:59
# @Author  : 高春阳
# @File    : models.py
# @Software: PyCharm

from app import db, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt

# User关注关联辅助表
followers = db.Table(
	'follower',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# 告知登录扩展flask-login login对象当前的用户对象
@login.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin, db.Model):
	# __tablename__ = 'm_users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	# 扩充字段
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow())
	# 关注
	followed = db.relationship(
		'User',
		secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'),
		lazy='dynamic'
	)

	def __repr__(self):
		# return '<User {}>'.format(self.username)
		return '<User {}, Email {}, Password_Hash {}, Post {}>'.format(self.username, self.email, self.password_hash,
																	   self.posts)

	# 密码设置与验证
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	# 头像
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	# 关注
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	# 取消关注
	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	# 是否关注
	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	# 当前用户已关注用户贴子的查询
	def followed_posts(self):
		# 1.用post表和follower表联合查询，条件是所有已经被关注user的所有post(followed_id==post.user_id)
		# 2.过滤出当前user所关注的user的所有的post(follower_id == self.id)
		# 3.按时间降序
		# return Post.query.join(followers, (followers.c.followed_id == Post.user_id)). \
		#     filter(followers.c.follower_id == self.id). \
		#     order_by(Post.timestamp.desc())
		followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)). \
			filter(followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(payload={'reset_password': self.id, 'exp': time() + expires_in},
						  key=app.config['SECRET_KEY'],
						  algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		result_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
		if 'reset_password' in result_data:
			user_id = result_data['reset_password']
			return User.query.get(user_id)


class Post(db.Model):
	# __tablename__ = 'm_posts'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(1024))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	# 语言
	language = db.Column(db.String(5))

	def __repr__(self):
		return '<Post {}>'.format(self.body)
