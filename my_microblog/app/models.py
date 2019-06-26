#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-17 15:59
# @Author  : 高春阳
# @File    : models.py
# @Software: PyCharm

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
	# __tablename__ = 'm_users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, passwrod):
		self.password_hash = generate_password_hash(passwrod)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class Post(db.Model):
	# __tablename__ = 'm_posts'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(1024))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)