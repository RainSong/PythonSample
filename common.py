# -*- coding:utf-8 -*-

import os
import binascii
import hashlib

user_name = '714224605@qq.com'
password = '@@dlr2016'

random = os.urandom(12)
print random
key = binascii.b2a_base64(random)
print key
salt = key[::-1]

salt = 'gRYbOsEqfwooO2tB'

print salt

def getmd5(strContent):
    """
    获取字符串的md5值
    :param strContent:
    :return:
    """
    strContent = strContent.encode()
    m = hashlib.md5()
    m.update(strContent)
    return m.hexdigest()

print getmd5(salt + getmd5(password))

print getmd5('gRYbOsEqfwooO2tB' + getmd5(password))