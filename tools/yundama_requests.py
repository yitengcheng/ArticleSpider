#!/usr/bin/env python
'''
@File    :   yundama_requests.py
@Time    :   2019/03/11 21:17:26
@Author  :   fan zehua 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import json
import requests


class YDMHttp(object):
    apiurl = 'http://api.yundama.com/api.php'
    username = 'ean7891'
    password = 'enengy2fan'
    appid = '7100'
    appkey = 'b8bdafee3e8562455cbb0f7f2ac18921'

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def balance(self):
        data = {
            'method': 'balance',
            'username': self.username,
            'password': self.password,
            'appid': self.appid,
            'appkey': self.appkey,
        }
        response_data = requests.post(self.apiurl, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data['ret'] == 0:
            print("获取剩余积分", ret_data["balance"])
            return ret_data["balance"]
        else:
            return None

    def login(self):
        data = {
            'method': 'login',
            'username': self.username,
            'password': self.password,
            'appid': self.appid,
            'appkey': self.appkey
        }
        response_data = requests.post(self.apiurl, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("登录成功", ret_data["uid"])
            return ret_data["uid"]
        else:
            return None

    def decode(self, filename, codetype, timeout):
        data = {
            'method': 'upload',
            'username': self.username,
            'password': self.password,
            'appid': self.appid,
            'appkey': self.appkey,
            'codetype': str(codetype),
            'timeout': str(timeout)
        }
        files = {'file': open(filename, 'rb')}
        response_data = requests.post(self.apiurl, files=files, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("识别成功", ret_data["text"])
            return ret_data["text"]
        else:
            return None
