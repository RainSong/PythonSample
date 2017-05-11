# -*- coding:utf-8 -*-

import os
import zipfile

path = 'D:\\website\\xiaoheima_publish_packages'
pwd = '123456'


def get_zip_files(path):
    files = os.listdir(path)
    zip_files = []
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and zipfile.is_zipfile(file_path):
            zip_files.append(file)
    return zip_files


def extracta_files(path, files, pwd):
    pwd = pwd.encode(encoding='utf-8')
    for file in files:
        zf = zipfile.ZipFile(os.path.join(path,file), 'r', zipfile.ZIP_DEFLATED)
        zf.extractall(path=path, pwd=pwd)
        zf.close()
        print('文件{0}解压完成'.format(file))


if __name__ == '__main__':
    zip_files = get_zip_files(path)
    extracta_files(path, zip_files, pwd)
    print('所有文件解压完成')
