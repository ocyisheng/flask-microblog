#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/29 10:53 AM
# @Author  : Gao
# @File    : translate.py
# @Software: PyCharm

from urllib import request, parse
import json

'''
有道翻译
http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=计算

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
# http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=计算
YOUDAO_TRANSLATE_API = 'http://fanyi.youdao.com/translate?&doctype=json&type={}&i={}'


def translate(q, from_lang, to_lang):
	l_type = lang_type(from_lang, to_lang)
	# 中文字符需要url编码
	q = parse.quote(q)
	url = YOUDAO_TRANSLATE_API.format(l_type, q)
	req = request.Request(url=url, method='GET')
	# req.add_header()
	with request.urlopen(req) as f:
		data = json.loads(f.read().decode('utf-8'))
		if data['errorCode'] == 0:
			return data['translateResult'][0][0]['tgt']


def lang_type(from_type, to_type):
	types = ['ZH', 'EN', 'JA', 'KR', 'FR', 'RU', 'SP']
	from_type = from_type.upper()[:2]
	to_type = to_type.upper()[:2]
	if from_type not in types or to_type not in types:
		return 'AUTO'
	if from_type == 'ZH':
		from_type = 'ZH_CN'
	if to_type == 'ZH':
		to_type = 'ZH_CN'
	return from_type + '2' + to_type


if __name__ == '__main__':
	print(translate('这个就是我的计算器。', 'zh', 'en'))
