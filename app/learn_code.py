#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 6:45 PM
# @Author  : Gao
# @File    : learn_code.py
# @Software: PyCharm

# 选择排序
def select_sort(arr):
	for i in range(len(arr) - 1):
		for j in range(i + 1, len(arr)):
			if arr[i] > arr[j]:
				temp = arr[i]
				arr[i] = arr[j]
				arr[j] = temp
		print(arr)


def bubble_sort(arr):
	for i in range(len(arr) - 1):
		for j in range(0, len(arr) - i - 1):
			if arr[j] > arr[j + 1]:
				temp = arr[j]
				arr[j] = arr[j + 1]
				arr[j + 1] = temp
		print(arr)


if __name__ == '__main__':
	test_arr1 = [23, 4, 67, 89, 8, 12, 34754, 907, 333, 124, 7, 65]
	test_arr2 = test_arr1.copy()
	select_sort(arr=test_arr1)
	print('................ ')
	bubble_sort(arr=test_arr2)
