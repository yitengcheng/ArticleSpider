# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from ArticleSpider.utils.common import get_nums
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + '-jobble'


def date_convert(value):
    try:
        create_date = datetime.datetime.strftime(value, '%Y/%m/%d').date()
    except:
        create_date = datetime.datetime.now().date()
    return create_date


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if '评论' in value:
        return ''
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(add_jobbole))
    create_date = scrapy.Field(input_processor=MapCompose(date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    img_url = scrapy.Field(output_processor=MapCompose(return_value))
    img_path = scrapy.Field()
    praise_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    comments_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(','))
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title,url,create_date,fav_nums,url_object_id,img_url,praise_nums,comments_nums,tags,content, img_path)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
          """
        params = (self["title"], self["url"], self["create_date"],
                  self["fav_nums"], self["url_object_id"], self["img_url"],
                  self["praise_nums"], self["comments_nums"], self["tags"],
                  self["content"], self['img_path'])
        return insert_sql, params


class CaoLiuArticleItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()
    img_name = scrapy.Field()
    img_path = scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
          """
        zhihu_id = self['zhihu_id'][0]
        topics = ','.join(self['topics'])
        url = ''.join(self['url'])
        title = ''.join(self['title'])
        content = ''.join(self['content'])
        answer_num = get_nums(''.join(self['answer_num']))
        comments_num = get_nums(''.join(self['comments_num']))
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        if len(self['watch_user_num']) == 2:
            watch_user_num = int(self['watch_user_num'][0])
            click_num = int(self['watch_user_num'][1])
        else:
            watch_user_num = int(self['watch_user_num'][0])
            click_num = 0

        params = (zhihu_id, topics, url, title, content, answer_num,
                  comments_num, watch_user_num, click_num, crawl_time)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
