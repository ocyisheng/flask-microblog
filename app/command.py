#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 6:37 PM
# @Author  : Gao
# @File    : command.py
# @Software: PyCharm
from app import app
import os
import click

'''
有道翻译
http://fanyi.baidu.com/transapi?from=auto&to=cht&query=Calculation

type的类型有：

ZH_CN2EN 中文　»　英语
ZH_CN2JA 中文　»　日语
ZH_CN2KR 中文　»　韩语
ZH_CN2FR 中文　»　法语
ZH_CN2RU 中文　»　俄语
ZH_CN2SP 中文　»　西语
EN2ZH_CN 英语　»　中文
JA2ZH_CN 日语　»　中文
KR2ZH_CN 韩语　»　中文
FR2ZH_CN 法语　»　中文
RU2ZH_CN 俄语　»　中文
SP2ZH_CN 西语　»　中文

'''

@app.cli.group(name='translate', help='Language localization')
def translate():
	# 翻译和本地化命令
	pass


@translate.command(name='init', help='Initial language localization')
# click添加参数
@click.argument('lang')
def init(lang):
	# 初始化一个新语言
	if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
		raise RuntimeError('extract command failed')
	if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
		raise RuntimeError('init command failed')
	os.remove('messages.pot')

@translate.command(name='update', help='Update language localization')
def update():
	# 更新所有语言
	if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
		raise RuntimeError('extract command failed')
	if os.system('pybabel update -i messages.pot -d app/translations'):
		raise RuntimeError('update command failed')
	os.remove('messages.pot')


@translate.command(name='compile', help='Complete language localization')
def compile():
	# 编译所有语言
	if os.system('pybabel compile -d app/translations'):
		raise RuntimeError('compile command failed')


def custom_command_init():
	print('import & init custom flask command')
