#!/usr/bin/env python
'''
@File    :   zhihu_sel.py
@Time    :   2019/02/23 19:41:57
@Author  :   fan zehua 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import requests
import http.cookiejar as cookielib
import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.text')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies未能加载')

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

header = {
    'HOST': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': agent
}


def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ''


def get_index():
    response = session.get('https://www.zhihu.com', headers=header)
    with open('index_page.html', 'wb') as f:
        f.write(response.text.encode('utf8'))
    print('ok')


def is_login():
    # 通过个人中心页面返回状态码判断是否为登录状态
    inbox_url = 'https://www.zhihu.com/inbox'
    # allow_redirects 是否重定向
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def zhihu_login(account, password):
    # 知乎登录
    if re.match('^1\d{10}', account):
        print('手机号登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            '_xsrf': get_xsrf(),
            'phone_num': account,
            'password': password,
        }
        response_text = session.post(post_url, data=post_data, headers=header)

        session.cookies.save()
