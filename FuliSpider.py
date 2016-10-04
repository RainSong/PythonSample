# -*- coding:utf-8 -*-

import getpass
from requests import session
from bs4 import BeautifulSoup
import logging
from logger import logger
import re


class FuliSpiter:
    session = None

    def __init__(self):
        self.session = session()

    def request(self, url, method='POST', responseCoding=None, data=None, headers=None):
        response = self.session.request(url=url, method=method, data=data, headers=headers)
        if responseCoding is None:
            return response.content
        return response.content.decode(responseCoding)

    def login(self):
        """
        登陆
        :param userName:
        :param password:
        :return:
        """
        login_url = 'https://fuli.us/wp-login.php'
        method = 'POST'
        data = {
            'log': '',
            'pwd': '',
            'wp - submit': '登录',
            'redirect_to': '/'
        }

        headers = {
            "User-Agent": "Mozilla/5.0(Windows NT 6.1; Win64; x64) AppleWebKit/537.36(KHTML,like Gecko)Chrome/52.0.2743.116 Safari/537.36"
        }
        loginSuccess = False
        while not loginSuccess:
            userName = input('用户名：')
            password = getpass.getpass('密码：')
            try:
                data['log']=userName
                data['pwd'] = password
                content = self.request(url=login_url, method=method, responseCoding='utf-8', data=data, headers=headers)
                p = re.compile('\<strong\>错误\<\/strong\>\：.*\。')
                match_result = p.search(content)
                if match_result is not None:
                    msg = match_result.group(0) \
                        .replace('<strong>错误</strong>：', '') \
                        .replace('。', '') \
                        .replace('<strong>', '') \
                        .replace('</strong>', '')
                    print('登陆失败：' + msg + '\n')
                else:
                    print('登陆成功\n')
            except Exception as e:
                logger.error('登陆失败', e)
                print('\n')



def readListPage(self, pageIndex=1):
    """
    爬去列表页
    :param pageIndex:
    :return:
    """
    if pageIndex == 1:
        url = 'https://fuli.us'
    else:
        url = 'https://fuli.us/page/{0}'.format(pageIndex)
    content = self.request(url, 'get')
    soup = BeautifulSoup(content, 'utf-8')


def readInfoPage(self, url):
    """
    爬取详细页
    :param url:
    :return:
    """
    pass


def pubComment(self):
    """
    发表评论
    :return:
    """
    pass


def getFileUrlAndPassword(self, url):
    """
    获取文件下载地址以及提取码
    :param url:
    :return:
    """
    fileUrl = ''
    code = ''
    return (fileUrl, code)


def downLoadFile(self, fileUrl, code):
    """
    下载文件
    :param fileUrl:
    :param code:
    :return:
    """
    pass  # https://fuli.us/page/2


if __name__ == '__main__':

    spiter = FuliSpiter()
    spiter.login()
    spiter.spit()
