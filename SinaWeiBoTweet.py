# -*- coding:utf-8 -*-

import json
import urllib
import os
import pickle
import requests
import re
import time
from SinaWeiBoLogin import weiboLogin


class Tweet():
    """

    """
    pub_url = 'http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd={0}'
    img_upload_url = 'http://picupload.service.weibo.com/interface/pic_upload.php' \
                     '?app=miniblog' \
                     '&data=1' \
                     '&url=weibo.com/u/6016530069' \
                     '&markpos=1' \
                     '&logo=1' \
                     '&nick=%40Mr-Roboter' \
                     '&marks=1' \
                     '&url=weibo.com/u/6016530069' \
                     '&markpos=1' \
                     '&logo=1' \
                     '&nick=%40Mr-Roboter' \
                     '&marks=1' \
                     '&url=weibo.com/u/6016530069' \
                     '&markpos=1' \
                     '&logo=1' \
                     '&nick=%40Mr-Roboter' \
                     '&marks=1' \
                     '&mime=image/jpeg' \
                     '&ct=0.455397117882967'
    cookies = None
    session = None

    def __init__(self, session=None):
        if session is not None:
            self.session = session
        else:
            self.session = requests.session()
            if not os.path.exists('weibo.cookies'):
                print('不存在Cookie文件weibo.cookies，请先登录...')
                exit(0)
            try:
                with open('weibo.cookies', 'rb') as f:
                    cookie_dict = pickle.load(f)
                    self.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
            except Exception as e:
                print('从文件中加载Cookie失败，错误原因：', e)

    def uploadImageStream(self, image, addWaterMark=False):
        if addWaterMark:
            url = 'http://picupload.service.weibo.com/interface/pic_upload.php' \
                  '?app=miniblog' \
                  '&data=1' \
                  '&url=weibo.com/u/6016530069' \
                  '&markpos=1' \
                  '&logo=1' \
                  '&nick=%40Mr-Roboter' \
                  '&marks=1' \
                  '&url=weibo.com/u/6016530069' \
                  '&markpos=1' \
                  '&logo=1' \
                  '&nick=%40Mr-Roboter' \
                  '&marks=1' \
                  '&url=weibo.com/u/6016530069' \
                  '&markpos=1' \
                  '&logo=1' \
                  '&nick=%40Mr-Roboter' \
                  '&marks=1' \
                  '&mime=image/jpeg' \
                  '&ct=0.455397117882967'

        else:
            url = "http://picupload.service.weibo.com/interface/pic_upload.php" \
                  "?rotate=0" \
                  "&app=miniblog" \
                  "&s=json" \
                  "&mime=image/jpeg" \
                  "&data=1" \
                  "&wm="

        try:
            with open(image, 'rb') as f:
                img_content = f.read()
            resp = self.session.post(url, data=img_content, cookies=self.cookies)
            upload_json = re.search('{.*}}', resp.text).group(0)
            result = json.loads(upload_json)
            code = result["code"]
            if code == "A00006":
                pid = result["data"]["pics"]["pic_1"]["pid"]
                return True, pid
            else:
                print('图片{0}上传失败'.format(image))
                return False, ''
        except Exception as e:
            print('图片{0}上传失败，错误原因：'.format(image), e)
            return False, ''

    def uploadImages(self, images):
        """
        提交图片文件
        :param file_name:
        :return:
        """
        if len(images) > 9:
            print('最多同时上传9张图片')
            images = images[0:9]
        pic_ids = ''
        for img in images:
            upload_ok, pic_id = self.uploadImageStream(img)
            if upload_ok:
                if len(pic_ids) > 0:
                    pic_ids += ' '
                pic_ids += pic_id
                # pic_ids.append(pic_id)
        return pic_ids

    def getTweetFormData(self, message, pic_ids):
        """
        构建发送微博的数据
        :param message:
        :param pic_ids:
        :return:
        """
        form_data = {
            'location': 'v6_content_home',
            'appkey': '',
            'style_type': '1',
            'pic_id': pic_ids,
            'text': message,
            'pdetail': '',
            'rank': '0',
            'rankid': '',
            'module': 'stissue',
            'pub_source': 'main_',
            'pub_type': 'dialog',
            '_t': '0'
        }
        return form_data

    def pub(self, message=None, images=None):
        pic_ids = None
        if images is not None and len(images) > 0:
            pic_ids = self.uploadImages(images)

        form_data = self.getTweetFormData(message, pic_ids)

        headers = {
            'Cache - Control': 'no-cache',
            'Content - Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://weibo.com/u/6016530069/home',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }

        seconds = int(time.time() * 1000)
        url = self.pub_url.format(seconds)
        try:
            response = self.session.post(url, data=form_data, headers=headers, cookies=self.cookies)
            result = json.loads(response.text)
            if result['code'] == '100000':
                print('微博发表成功')
            else:
                print('微博发表失败')
        except Exception as e:
            print('微博发表失败，错误原因：', e)
            # print(response.content.decode('utf-8'))


if __name__ == '__main__':
    login = weiboLogin()
    user_id, session = login.login()

    # images = ['D:\\Users\\YGJ\\Pictures\\GlowingBeaches\\5.jpg',
    #           'D:\\Users\\YGJ\\Pictures\\GlowingBeaches\\6.jpg']
    # message = input('请输入要发送的微博内容：')
    # tweet = Tweet(session=session)
    # tweet.pub(message, images)
