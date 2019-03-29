# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import CaoLiuArticleItem, ArticleItemLoader


class CaoliuSpider(scrapy.Spider):
    name = 'caoliu'
    allowed_domains = ['hs.dety.men']
    start_urls = ['https://hs.dety.men/thread0806.php?fid=16&search=&page=100']

    def parse(self, response):
        post_urls = response.xpath(
            '//*[@id="ajaxtable"]//tr[@class="tr3 t_one tac"]//td[@class="tal"]\
                /h3/a/@href').extract()
        for post_url in post_urls:
            yield Request(
                url=parse.urljoin(response.url, post_url),
                callback=self.parse_detail,
                dont_filter=True)
        next_url = response.xpath(
            '//*[@id="main"]/table[1]/tr/td[1]/div/a[2]/@href').extract_first()
        if next_url:
            next_url = parse.urljoin(response.url, next_url)
            yield Request(url=next_url, callback=self.parse, dont_filter=True)
        pass

    def parse_detail(self, response):
        images = response.css('input[type="image"]::attr("data-src")\
            ').extract()
        item_loader = ArticleItemLoader(
            item=CaoLiuArticleItem(), response=response)
        item_loader.add_xpath(
            'title',
            '//*[@id="main"]/div[3]/table/tr[1]/th[2]/table/tr/td/h4/text()')
        item_loader.add_value('img_url', [images])
        article_item = item_loader.load_item()
        yield article_item

        pass
