#!/usr/bin/env python
'''
@File    :   common.py
@Time    :   2019/02/17 22:34:22
@Author  :   fan zehua
@Version :   1.0
@Contact :   316679581@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import hashlib
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# MD5摘要生成


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_nums(value):
    # 从字符串中截取数字
    match_re = re.match(r".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


# 生成selenium 浏览器对象
def get_browser():
    chrome_option = Options()
    chrome_option.add_argument('--disable-extensions')
    chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    browser = webdriver.Chrome(
        executable_path='/usr/bin/chromedriver', chrome_options=chrome_option)
    return browser
