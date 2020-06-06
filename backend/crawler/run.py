import os
import time

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from celery import shared_task

from backend.crawler.crawler.utils import get_config, update_config
from ..models import Content


@shared_task()
def run(kw, source):
    os.chdir('/home/respeaker/LiteratureRetrieval/backend/crawler')

    names = source
    project_settings = get_project_settings()
    process = CrawlerProcess(project_settings)

    for name in names:
        custom_settings = get_config(name)
        custom_settings['start_urls']['args'] = [kw]
        update_config(name, custom_settings)

        spider = custom_settings.get('spider', 'literature')
        process.crawl(spider, **{'name': name})

    process.start(stop_after_crawl=False)


class Worker:
    def __init__(self, kw, source):
        self.kw = kw
        self.source = source

    def get_data(self, page_num, page_size):
        print('判断是否为第一次请求')
        if self.is_first_request():
            Content.objects.all().delete()

            print('启动爬虫')
            now = time.time()
            # 启动爬虫
            spider = run.delay(self.kw, self.source)

            print('启动完成,用时{}'.format(time.time()-now))
            i = 0
            while not self.data_count():
                if i >= 10:
                    break
                i = i + 1
                time.sleep(1)

        # 从数据库获取数据
        data = Content.objects.values('title', 'authors', 'brief', 'source', 'website')
        paginator = Paginator(data, page_size)

        try:
            literature = paginator.page(page_num)
        except PageNotAnInteger:
            literature = paginator.page(1)
        except EmptyPage:
            literature = paginator.page(paginator.num_pages)

        literature = list(literature)

        for index, item in enumerate(literature):
            sources = item['source'].split('||')
            websites = item['website'].split('||')
            literature[index]['sources'] = [{'link': link, 'name': name} for (link, name) in zip(sources, websites)]
        return literature, self.data_count()

    def is_first_request(self):
        custom_settings = get_config(self.source[0])

        return custom_settings['start_urls']['args'][0] != self.kw

    @staticmethod
    def data_count():
        return Content.objects.all().count()


if __name__ == '__main__':
    now = time.time()
    run('计算机')
    print(time.time()-now)
