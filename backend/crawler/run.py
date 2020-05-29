import os
import time

import pymysql

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from django.conf import settings
from celery import shared_task

from backend.crawler.crawler.utils import get_config, update_config


@shared_task()
def run(kw):
    os.chdir('/home/respeaker/LiteratureRetrieval/backend/crawler')

    names = ['wf', 'ixs']
    project_settings = get_project_settings()
    process = CrawlerProcess(project_settings)

    for name in names:
        custom_settings = get_config(name)
        custom_settings['start_urls']['args'] = [kw]
        update_config(name, custom_settings)

        spider = custom_settings.get('spider', 'literature')
        process.crawl(spider, **{'name': name})

    process.start(stop_after_crawl=False)


class Worker():
    def __init__(self, kw):
        self.conn = pymysql.connect(
            host=settings.HOST,
            user=settings.USER,
            passwd=settings.PASSWORD,
            db=settings.DB_NAME
        )
        self.cursor = self.conn.cursor()
        self.kw = kw

    def get_data(self, page_num, page_size):
        if self.is_first_request():
            # 启动爬虫
            run.delay(self.kw)

            i = 0
            while self.has_data() == 0:
                print('wait')
                time.sleep(1)
                i = i + 1
                if i > 5:
                    break
        sql = "SELECT * FROM content LIMIT {}, {}".format((page_num-1)*page_size, page_size)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def is_first_request(self):
        custom_settings = get_config('wf')
        if custom_settings['start_urls']['args'][0] == self.kw:
            return False
        else:
            return True

    def has_data(self):
        sql = "SELECT * FROM content"
        self.cursor.execute(sql)
        return len(self.cursor.fetchall())

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    now = time.time()
    run('word2vec')
    print(time.time()-now)
