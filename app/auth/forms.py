#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 2:11 AM
# @Author  : Gao
# @File    : forms.py
# @Software: PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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
	submit = SubmitField(_l('Request Mailbox Verification'))

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError(_l('Your email have not registed !'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('New Password', validators=[DataRequired()]))
	password2 = PasswordField(_l('Repeate New Password', validators=[DataRequired(), EqualTo('password')]))
	submit = SubmitField(_l('Request Password Reset'))
