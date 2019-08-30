#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 17:01
# @Author  : 高春阳
# @File    : froms.py
# @Software: PyCharm

from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf import FlaskForm
from app.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember_Me'), default=False)
	submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
	username = StringField(_l('Username', validators=[DataRequired()]))
	email = StringField(_l('Email', validators=[DataRequired(), Email()]))
	password = PasswordField(_l('Password', validators=[DataRequired()]))
	password2 = PasswordField(_l('Repeat Password', validators=[DataRequired(), EqualTo('password')]))
	submit = SubmitField(_l('Register'))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError(_l('Please use a different username .'))

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError(_l('Please use a different email address .'))


class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email', validators=[DataRequired(), Email()]))
	submit = SubmitField(_l('Request Password Reset'))

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError(_l('Your email have not registed !'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password', validators=[DataRequired()]))
	password2 = PasswordField(_l('Repeate Password', validators=[DataRequired(), EqualTo('password')]))
	submit = SubmitField(_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
	username = StringField(_l('Username', validators=[DataRequired()]))
	about_me = TextAreaField(_l('About Me', validators=[Length(min=0, max=140)]))
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError(_l('Please use a different username .'))


class PostForm(FlaskForm):
	post = TextAreaField(_l('Say something', validators=[DataRequired(), Length(min=1, max=140)]))
	submit = SubmitField(_l('Submit'))
