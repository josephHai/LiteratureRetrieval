import time
import logging

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from celery import shared_task
from django.core.cache import cache
from pyhanlp import *
from jpype import *
from nltk.corpus import stopwords

from backend.crawler.crawler.utils import get_config, update_config
from ..models import Content


logger = logging.getLogger(__name__)


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
        self.source = source
        self.kw = self.handle_kw(kw)

    def get_data(self, page_num, page_size):
        if self.kw == '':
            return [], 0
        logger.info('当前关键词为: {}'.format(self.kw))
        logger.info('判断是否为第一次请求')
        if self.is_first_request():
            Content.objects.all().delete()

            logger.info('启动爬虫')
            current = time.time()
            # 启动爬虫
            run.delay(self.kw, self.source)

            logger.info('启动完成,用时{}'.format(time.time() - current))
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
            links = list(set(sources))
            links.sort(key=sources.index)
            names = list(set(websites))
            names.sort(key=websites.index)
            literature[index]['sources'] = [{'link': link, 'name': name} for (link, name) in zip(sources, websites)]
        return literature, self.data_count()

    def is_first_request(self):
        if cache.has_key('kw') and cache.get('kw') == self.kw:
            return False
        else:
            cache.set('kw', self.kw)
            return True

    @staticmethod
    def handle_kw(kw, top=10):
        s1 = []
        allow_pos = ['g', 'gb', 'gbc', 'gc', 'gg', 'gi', 'gm', 'gp', 'n', 'nb', 'nba', 'nbc', 'nbp', 'nf', 'ng', 'nh',
                     'nhd', 'nhm', 'ni', 'nic', 'nis', 'nit', 'nl', 'nm', 'nmc', 'nn', 'nnd', 'nnt', 'nr', 'nr1', 'nr2',
                     'nrf', 'nrj', 'ns', 'nsf', 'nt', 'ntc', 'ntcb', 'ntcf', 'ntch', 'nth', 'nto', 'nts', 'ntu', 'nx',
                     'nz']
        stop_words = stopwords.words('chinese')
        IndexTokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
        for term in IndexTokenizer.segment(kw):
            word, pos = term.word, term.nature
            if word not in stop_words and pos.__str__() in allow_pos:
                s1.append(word)
        return ' '.join(s1)

    @staticmethod
    def data_count():
        return Content.objects.all().count()


if __name__ == '__main__':
    now = time.time()
    run('计算机', ['wp'])
    print(time.time() - now)
