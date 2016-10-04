# -*- coding:utf-8 -*-

import base64
import binascii
import json
import os
import pickle
import re
import requests
import rsa
import time
import urllib
from urllib import parse


class weiboLogin:
    """
    新浪微博的模拟登陆
    """
    session = None
    cookies = None

    def __init__(self):
        self.login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.pre_login_url = 'https://login.sina.com.cn/sso/prelogin.php' \
                             '?entry=weibo' \
                             '&callback=sinaSSOController.preloginCallBack' \
                             '&su={0}' \
                             '&rsakt=mod' \
                             '&checkpin=1' \
                             '&client=ssologin.js(v1.4.18)' \
                             '&_={1}'
        self.session = requests.Session()

    def getServerData(self, username):
        """
        获取预登陆数据
        :param: username
        :return: servertime
        :return: nonce
        :return: pubkey
        :return: rsakv
        """
        uname = base64.b64encode(username.encode('utf-8'))
        seconds = int(time.time())
        url = self.pre_login_url.format(uname, seconds)

        response = self.session.get(url)
        data = response.content.decode('utf-8')
        p = re.compile('\{(\w*\W*\d*)+\}')
        try:
            json_data = p.search(data).group(0)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            print('获取预登陆信息成功')
            return servertime, nonce, pubkey, rsakv
        except Exception as e:
            print('获取预登陆信息失败，错误信息：' + e.args)
            return None

    def encryptPassword(self, password, servertime, nonce, pubkey):
        """
        加密密码
        :param password:
        :param servertime:
        :param nonce:
        :param pubkey:
        :return: password
        """
        print('加密密码')

        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        pwd = rsa.encrypt(message.encode('utf-8'), key)  # 加密
        pwd = binascii.b2a_hex(pwd)  # 将加密信息转换为16进制。
        return pwd

    def getLoginFormData(self, userName, password, servertime, nonce, rsakv):
        """
        获取登陆需要提交的表单数据
        :param userName:
        :param password:
        :param servertime:
        :param nonce:
        :param rsakv:
        :return:
        """
        form_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': 'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
            'vsnf': '1',
            'su': base64.b64encode(requests.utils.quote(userName).encode('utf-8')),
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        # form_data = urllib.parse.urlencode(form_data)
        return form_data

    def getLoginRedirectUrl(self, uname, psw, servertime, nonce, pubkey, rsakv):
        """
        获取登陆重定向URL
        :return:
        """
        formData = self.getLoginFormData(uname, psw, servertime, nonce, rsakv)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.sina.com.cn",
            "Origin": "http://open.weibo.com",
            "Referer": "http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E",
            "Upgrade-Insecure-Requests": "1"
        }
        try:
            response = self.session.post(url=self.login_url, data=formData, headers=headers)
            self.cookies = response.cookies
            content = response.content.decode('gbk')

            p = re.compile('location\.replace[\("].*[\")]')
            login_redirect_url = p.search(content).group(0)
            login_redirect_url = login_redirect_url.replace('location.replace(\'', '').replace('\');})', '')
            login_redirect_url = login_redirect_url.replace('location.replace(\"', '').replace('\")', '')
            print('获取登陆重定向URL成功：' + login_redirect_url)
            return login_redirect_url

        except Exception as e:
            print('提交登陆信息失败，错误原因：', e)
            return None

    def loadCookies(self):
        """
        从文件中加载Cookies
        :return:
        """
        try:
            with open('weibo.cookies', 'rb') as f:
                cookie_dict = pickle.load(f)
                cookies = requests.utils.cookiejar_from_dict(cookie_dict)
        except Exception as e:
            print('加载Cookies文件失败，错误原因：', e)
        return cookies

    def saveCookies(self):
        """
        保存Cookies到文件
        :return:
        """
        try:
            with open('weibo.cookies', 'wb') as f:
                dict_cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
                pickle.dump(dict_cookies, f)

                print('保存Cookies到文件weibo.cookies')
        except IOError as e:
            print('保存Cookies到文件weibo.cookies失败，错误原因：', e)

    def inputUserNamePassword(self):
        """
        提示输入用户名密码
        :return:
        :return:
        """
        print('新浪微博模拟登陆:')
        username = input(u'用户名：')
        password = input(u'密码：')

        return username, password

    def checkLogin(self):
        """
        检查登陆状态
        :return:
        """
        if not os.path.exists('weibo.cookies'):
            return False
        cookies = self.loadCookies()
        if cookies is None:
            return False
        # cookies = None
        response = self.session.get('http://passport.weibo.com/wbsso/login?ssosavestate=1506410191&url=http%3A%2F%2Fweibo.com%2F&ticket=ST-NjAxNjUzMDA2OQ==-1474874191-xd-13E967A3FB06C2A374653BD236748220&retcode=0', cookies=cookies)
        return False

    def login(self):

        if self.checkLogin():
            return '', self.session

        username, password = self.inputUserNamePassword()

        servertime, nonce, pubkey, rsakv = self.getServerData(username)

        pwd = self.encryptPassword(password, servertime, nonce, pubkey)

        login_url = self.getLoginRedirectUrl(username, pwd, servertime, nonce, pubkey, rsakv)

        try:
            response = self.session.get(login_url)
            content = response.content.decode('gb2312')
            p = re.compile('\{.*\}')
            json_data = p.search(content).group(0)
            data = json.loads(json_data)
            user_id = data['userinfo']['uniqueid']
            if data['result']:
                print('登陆成功')
                self.cookies = response.cookies
                self.saveCookies()
                return user_id, self.session
        except Exception as e:
            print("登陆失败，错误原因", e)
