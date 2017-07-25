# -*- coding:utf-8 -*-

import os
import binascii
import hashlib

user_name = '714224605@qq.com'
password = '@@dlr2016'

random = os.urandom(12)
print
random
key = binascii.b2a_base64(random)
print
key
salt = key[::-1]

salt = 'gRYbOsEqfwooO2tB'

print
salt


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


print
getmd5(salt + getmd5(password))

print
getmd5('gRYbOsEqfwooO2tB' + getmd5(password))

def row2dict(row):
    """
    将sqlalchemy中的一个对象转换为字典类型
    :param row:
    :return:
    """
    if row is None:
        return None
    dic = {}
    if hasattr(row,'__table__'):
        for column in row.__table__.columns:
            value = get_col_value(row,column.name)
            if value is None:
                continue
            dic[column.name] = value
    elif hasattr(row,'_fields'):
        for field in row._fields:
            value = get_col_value(row,field)
            if value is None:
                continue
            dic[field] = value
    return dic

def rows2dictList(result):
    """
    将Sqlalchemy结果集转换为一个字典列表
    :param result:Sqlalchemy结果集
    :return:字典列表
    """
    if result is None:
        return None
    dics = []
    for row in result:
        if row is None:
            continue
        dic = row2dict(row)
        dics.append(dic)

    return dics
