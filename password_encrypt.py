# -*- encoding:utf-8 -*-


import hashlib
import os
import binascii


def getmd5(str):
    str = str.encode()
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

salt = os.urandom(12)
salt = binascii.hexlify(salt)
salt = salt.decode()
salt = salt[::-1]

print(salt)

password = 'admin'
password = getmd5(salt + getmd5(password))
print(password)

