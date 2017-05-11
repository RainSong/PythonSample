# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
import time
import io

oldPath = 'D:\\website\\xiaoheima\\'
basePath = 'D:\\website\\publish\\'
packagePath = 'D:\\website\\xiaoheima_publish_packages\\'
logPath = 'D:\\website\\xiaoheima_publish_logs\\'

removeDirs = [
    '\\aspnet_client',
    '\\log',
    '\\packages',
    '\\Temp',
    '\\images',
    '\\img',
    '\\upfile',
    '\\uploadfiles',
    '\\Configs',
    '\\trunk',
    '\\action\\xinnian\\images',
    '\\cct_member\\images',
    '\\cct_member\\uploadfiles',
    '\\cct_member\\uploadproduct',
    '\\heima_member\\images',
    '\\heima_member\\uploadfiles',
    '\\heima_member\\uploadproduct',
    '\\mobile\\images\\types'
]

removeFiles = [
    '\\Web.config',
    '\\xiaoheima.sln',
    '\\xiaoheima2010.sln',
    '\\xiaoheima2013.sln'
]

logFile = open(logPath + time.strftime('%Y%m%d%H%M', time.localtime(time.time())), 'w')


def remove(basePath, removePaths, type):
    """移除无用的文件"""
    for dir in removePaths:
        tempPath = basePath + dir
        if os.path.exists(tempPath):
            try:
                if (type == '文件'):
                    os.remove(tempPath)
                else:
                    shutil.rmtree(tempPath)
                    msg = "删除{0}{1}成功".format(type, dir)
                    log(msg)
            except Exception as e:
                msg = "删除{0}{1}失败;{2}".format(type, dir, e)
                log(msg)
        else:
            msg = "{0}{1}不存在，跳过".format(type, dir)
            log(msg)


def copy():
    """复制文件"""
    for dir in os.listdir(oldPath):
        tempPath = oldPath + dir
        if os.path.isfile(tempPath):
            shutil.copy(tempPath, basePath + dir)
            msg = '拷贝文件' + dir
            log(msg)
        else:
            shutil.copytree(tempPath, basePath + dir)
            msg = '拷贝目录' + dir
            log(msg)


def removeOld():
    """删除就文件"""
    for dir in os.listdir(basePath):
        tempPath = basePath + dir
        if os.path.isfile(tempPath):
            os.remove(tempPath)
            msg = '删除旧文件' + dir
            log(msg)
        else:
            shutil.rmtree(tempPath)
            msg = '删除旧目录' + dir
            log(msg)


def publish():
    """发布文件"""
    if not os.path.exists(basePath):
        os.mkdir(basePath)
        msg = "创建目录" + basePath
        log(msg)
    else:
        removeOld()
    copy()
    remove(basePath, removeDirs, '目录')
    remove(basePath, removeFiles, '文件')
    msg = '发布文件部署完成'
    log(msg)


def compress():
    """压缩文件"""
    strTime = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    with zipfile.ZipFile(packagePath + 'package' + strTime + '.zip', 'w', zipfile.ZIP_STORED) as zipFile:
        for root, dirs, files in os.walk(basePath):
            for file in files:
                zipFile.write(os.path.join(root, file))
                msg = '压缩文件：' + file
                log(msg)
    log('压缩完成')


def log(msg):
    """输出信息，记载日志
    Args:
        msg:要输出和记录的日志信息
    """
    logFile.write(msg + '\r')
    print(msg)


if __name__ == '__main__':
    publish()
    compress()

    log('生成更新包完成')

    if logFile is not None:
        logFile.close()
    exit(0)
