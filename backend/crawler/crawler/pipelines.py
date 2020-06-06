# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import logging

from django.db import connection
from scrapy.utils.project import get_project_settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiteratureRetrieval.settings')


class MySqlPipeline(object):
    def __init__(self):
        self.cursor = connection.cursor()
        self.sql = "INSERT INTO backend_content(`title`, `authors`, `brief`, `source`, `website`) " \
                   "VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE source=CONCAT(source, '||', VALUES(source)), " \
                   "website=CONCAT(website, '||', VALUES(website))"

    def process_item(self, item, spider):
        param = (item['title'], item['authors'], item['brief'], item['source'], item['website'])
        spider.sql_list.append(param)

        max_sql_num = get_project_settings()['MIN_SQL_NUM']
        if len(spider.sql_list) >= max_sql_num:
            self._insert(spider)

    def close_spider(self, spider):
        if spider.sql_list:
            self._insert(spider)
        self.cursor.close()

    def _insert(self, spider):
        spider.log('已爬取{}条数据，正在写入数据库'.format(len(spider.sql_list)), level=logging.INFO)
        self.cursor.executemany(self.sql, spider.sql_list)
        spider.sql_list.clear()
        connection.commit()
