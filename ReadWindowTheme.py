# -*- coding:utf-8 -*-

import os

theme_directory = 'H:\\Win7主题'


def read_theme_files():
    """
    show all files in directory
    :return:
    """
    for i in os.listdir(theme_directory):
        print(i+"\r")


if __name__ == '__main__':
    read_theme_files()

    key_input = input()
