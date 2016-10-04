# -*- coding:utf-8 -*-

def foo_throw_error():
	raise Exception('this method throw a error')

try:
	foo_throw_error()
	print 'no error'
except Exception as e:
	print Exception('this is a error',e)