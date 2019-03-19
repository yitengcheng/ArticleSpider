# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 放入待爬取的所有url

    def parse(self, response):
        """
        1. 获取文章列表页中的文章URL并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载
        """

        # 获取文章列表页中的文章URL并交给scrapy下载后并进行解析
        # 获取标签属性需要使用伪类::attr(属性名)
        post_nodes = response.css(
            '#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            # parse.urljoin(response.url, post_url)域名拼接函数
            # yield关键字就可以把Request交给scrapy进行下载
            yield Request(url=post_url, meta={'img_url': image_url}, callback=self.parse_detail)
        # 获取下一页的url并交给scrapy进行下载
        next_url = response.css(
            '.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段
        img_url = response.meta.get('img_url', '')
        # 实例化item
        article_item = JobBoleArticleItem()
        # 通过item Loader 加载item
        item_loader = ArticleItemLoader(
            item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        item_loader.add_value('img_url',  [img_url])
        item_loader.add_css(
            'praise_nums',  '.btn-bluet-bigger.href-style.vote-post-up.register-user-only h10::text')
        item_loader.add_css('fav_nums', 'span[data-book-type="1"]::text')
        item_loader.add_css(
            'comments_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', 'div.entry')
        article_item = item_loader.load_item()
        yield article_item
