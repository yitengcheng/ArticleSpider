# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.utils.common import get_browser
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os
from ArticleSpider.items import ArticleItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5
from datetime import datetime


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
        item_loader = ArticleItemLoader(item=LagouJobItem(), response=response)
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        item_loader.add_css('title', '.job-name::attr(title)')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('salary', '.job_request .salary::text')
        item_loader.add_xpath(
            'job_city', '/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')
        item_loader.add_xpath(
            'work_years', '/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')
        item_loader.add_xpath(
            'degree_need',
            '/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')
        item_loader.add_xpath(
            'job_type', '/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')
        item_loader.add_css('tags', '.position-label li::text')
        item_loader.add_css('publish_time', '.publish_time::text')
        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_desc', '.job-detail p')
        item_loader.add_css('job_address', '.work_addr')
        item_loader.add_css('company_name', '#job_company dt a img::attr(alt)')
        item_loader.add_css('company_url', '#job_company dt a::attr(href)')
        item_loader.add_value('crawl_time', datetime.now())
        return item_loader.load_item()
