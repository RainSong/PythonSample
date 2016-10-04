# -*- coding:utf-8 -*-

import os

files = [
    {
        'path': '''H:\\Test\\Abc\\a.aatv''',
        'size': 1024 * 1024 * 1024 * 2  # 2GB
    },
    {
        'path': '''H:\\Test\\Abc\\b.aatv''',
        'size': 1024 * 1024 * 1024  # 1GB
    },
    {
        'path': '''H:\\Test\\Abc\\Def\\c.aatv''',
        'size': 1024 * 1024 * 1024 * 2  # 2 GB
    },
    {
        'path': '''H:\\Test\\Abc\\Def\\e.aatv''',
        'size': 1024 * 1024 * 1024 * 2  # 2GB
    },
    {
        'path': '''H:\\Test\\Abc\\Def\\e.aatv''',
        'size': 1024 * 1024 * 1024 * 1  # 1GB
    },
    {
        'path': '''H:\\Test\\Abc\\Def\\f.aatv''',
        'size': 1024 * 1024 * 1024 * 1  # 1GB
    },
    {
        'path': '''H:\\Test\\Abc\\Def\\g.aatv''',
        'size': 1024 * 1024 * 1024 * 1  # GB
    }
]


def create_directory(path):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def writ_file(path, size):
    create_directory(path)
    file = open(path, 'w')
    file.seek(size)
    file.write('\x00')
    file.close()


def delete_dir():
    if os.path.exists('''H:\\Test'''):
        os.remove('''H:\\Test''')


def create_files():
    for item in files:
        writ_file(item.get('path'), item.get('size'))


if __name__ == '__main__':
    delete_dir()
    create_files()
