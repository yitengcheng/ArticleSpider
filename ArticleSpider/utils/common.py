#!/usr/bin/env python
'''
@File    :   common.py
@Time    :   2019/02/17 22:34:22
@Author  :   fan zehua
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import hashlib
# MD5摘要生成


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
