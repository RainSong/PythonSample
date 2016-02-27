# -*- coding: utf-8 -*-

import os
from datetime import *

prefix = "DC_"
path = "D:\TDDownload\dhmgdd\dhmgddgpscbfmsxjypyercmzh\imgs\\"
files = []

def getNewName():
   return prefix + datetime.now().strftime("%Y%m%d%H%M%S%f").replace('20160127','20150123')

def getExtensionName(fileName):
    names = fileName.split(".")
    if len(names) >= 2:
        return names[-1]
    return ''

def getFiles(path):
    if not os.path.exists(path):
        print '不存在目录：{0}'.format(path)
        exit(0)
    tempfiles = os.listdir(path)
    for f in tempfiles:
        if(os.path.isfile(path+f)):
            files.append(f)
    return files

if __name__=="__main__":
    files = getFiles(path)
    if len(files)==0:
        print("文件夹下没有文件")
        exit(0)
    for f in files:
        newname = path + getNewName() + "." + getExtensionName(f)
        os.rename(path+f,newname)

