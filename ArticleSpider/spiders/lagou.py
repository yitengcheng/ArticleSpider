# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.utils.common import get_browser
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    '''
        allow 符合这个格式的url就进行爬取
        deny 不符合这个格式的url就进行爬取
        allow_domains 符合这个域名的url就进行爬取
        deny_domains 不符合这个域名的url就进行爬取
        restrict_xpaths 通过xpath进一步限定url来源
        restrict_css 通过css进一步限定url来源
        tags 从什么标签去寻找url
        attrs 从标签的什么属性去提取url
    '''
    rules = (
        Rule(
            LinkExtractor(allow=r'jobs/\d+.html'),
            callback='parse_job',
            follow=True),
        Rule(LinkExtractor(allow=(r'zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=(r'gongsi/\d+.html',)), follow=True),
    )

    def start_requests(self):
        browser = get_browser()
        browser.get(self.start_urls[0])
        login_success = False
        try:
            browser.find_element_by_xpath(
                '//*[@id="changeCityBox"]/p[1]/a').click()
            time.sleep(5)
        except:
            pass
        try:
            browser.find_element_by_id('loginToolBar')
        except:
            login_success = True

        while not login_success:
            browser.find_element_by_xpath(
                '//*[@id="loginToolBar"]/div/div/a[1]').click()
            time.sleep(5)
            browser.find_element_by_id('email').send_keys('13984387205')
            browser.find_element_by_id('password').send_keys('energy2fan')
            browser.find_element_by_xpath(
                '//*[@id="loginPop"]/div[1]/form[1]/div[5]/input').click()
            time.sleep(10)
            login_success = True
        cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict)

    def parse_job(self, response):
        # 解析拉勾网的职位
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
