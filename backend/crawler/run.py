from scrapy.utils.project import get_project_settings
from backend.crawler.crawler.utils import get_config, update_config
from scrapy.crawler import CrawlerProcess
import time


def run(kw):
    names = ['wf', 'ixs']
    project_settings = get_project_settings()
    process = CrawlerProcess(project_settings)

    for name in names:
        custom_settings = get_config(name)
        custom_settings['start_urls']['args'] = [kw]
        update_config(name, custom_settings)

        spider = custom_settings.get('spider', 'literature')
        process.crawl(spider, **{'name': name})

    process.start()


if __name__ == '__main__':
    now = time.time()
    run('word2vec')
    print(time.time()-now)
