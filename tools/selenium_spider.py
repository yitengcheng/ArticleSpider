#!/usr/bin/env python
'''
@File    :   selenium_spider.py
@Time    :   2019/02/22 22:02:22
@Author  :   fan zehua 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome('E:/chromdriver/chromedriver.exe')

# browser.get('https://hs.dety.men/index.php')
# t_selector = Selector(text=browser.page_source)
# title = t_selector.css('#cate_1 .tr3.f_one th h2 a::text').extract()
browser.get('https://www.zhihu.com/signup?next=%2F')
# .click()点击元素
browser.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
# send_keys()向目标节点输入内容
browser.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys('13984387205')
browser.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('energy2fan')
browser.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()

browser.quit()
