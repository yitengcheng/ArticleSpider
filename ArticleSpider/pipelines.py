# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
import shutil
import scrapy

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from ArticleSpider.utils.common import get_md5
# 导入scrapy框架的图片下载类
import os
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):

    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # dict()创建一个字典
        # dumps()将python数据格式转换成字符串
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):

    def __init__(self):
        # 连接mysql数据库 MySQLdb.connect('host', 'user', 'password', 'dbname',charset='utf8')
        self.conn = MySQLdb.connect(
            '127.0.0.1',
            'root',
            'root',
            'article_spider',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 同步操作插入数据库
        insert_sql = """
            insert into jobbole_article(title,url,create_date,fav_nums)
            VALUES(%s,%s,%s,%s)
        """
        self.cursor.execute(
            insert_sql,
            (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted 将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 具体插入逻辑
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class ArticleImagePipeline(ImagesPipeline):
    # 从项目设置文件中导入图片下载路径
    img_store = get_project_settings().get('IMAGES_STORE')

    # 重写ImagesPipeline类的此方法
    # 发送图片下载请求
    def get_media_requests(self, item, info):
        img_urls = item['img_url']
        for img_url in img_urls:
            item["img_name"] = get_md5(img_url)
            yield scrapy.Request(img_url)

    # 重写item_completed方法
    # 将下载的文件保存到不同的目录中
    # def item_completed(self, results, item, info):
    #     image_path = [x["path"] for ok, x in results if ok]

    #     # 定义分类保存的路径
    #     img_path = "%s%s" % (self.img_store, item['img_path'])
    #     # 目录不存在则创建目录
    #     if os.path.exists(img_path) == False:
    #         os.mkdir(img_path)

    #     # 将文件从默认下路路径移动到指定路径下
    #     shutil.move(self.img_store +
    #                 image_path[0], img_path + "\\" + item["img_name"] + '.jpg')

    #     item["img_path"] = img_path + "\\" + item["img_name"] + '.jpg'
    #     return item
    # item_completed获取图片下载后的地址

    # def item_completed(self, results, item, info):
    #     if 'img_url' in item:
    #         for ok, value in results:
    #             image_file_path = value["path"]
    #         item["image_file_path"] = image_file_path
    #     return item
