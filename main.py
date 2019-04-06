#!/usr/bin/env python3
'''
@File    :   main.py
@Time    :   2019/02/02 10:14:03
@Author  :   fan zehua 
@Version :   1.0
@Contact :   316679581@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from scrapy.cmdline import execute
import sys
import os

# os.path获取文件路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "caoliu"])
# execute(["scrapy", "crawl", "zhihu"])
execute(["scrapy", "crawl", "lagou"])
