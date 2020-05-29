# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging

from django.conf import settings


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MySqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.HOST,
            user=settings.USER,
            passwd=settings.PASSWORD,
            db=settings.DB_NAME
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO content(`title`, `authors`, `brief`, `source`, `website`) VALUES(%s, %s, %s, %s, %s)" \
              "ON DUPLICATE KEY UPDATE source=CONCAT(source, '||', VALUES(source)), " \
              "website=CONCAT(website, '||', VALUES(website))"
        param = (item['title'], item['authors'], item['brief'], item['source'], item['website'])
        spider.param_list.append(param)

        if len(spider.param_list) >= 10:
            spider.log('已爬取10条数据，正在写入数据库', level=logging.INFO)
            self.cursor.executemany(sql, spider.param_list)
            spider.param_list.clear()
            self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
