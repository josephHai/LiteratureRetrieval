import requests
from lxml import etree
from enum import Enum
from backend.models import LiteratureItem, LiteratureList
import time


def response(url, params):
    html = requests.get(url, params).text
    return etree.HTML(html)


class Crawler:

    def __init__(self, text, page):
        self.keywords = text
        self.page = page
        self.page_size = 10
        self.literature_list = LiteratureList()

    def worker(self, source):
        switch = {
            self.SourceType.WF: self.wf_parse,
            self.SourceType.WP: self.wp_parse
        }

        switch[source]()

    def wf_parse(self):
        base_url = 'http://www.wanfangdata.com.cn'
        url = base_url + '/search/searchList.do'
        params = {
            'page': self.page,
            'searchWord': self.keywords,
            'pageSize': self.page_size
        }
        html = response(url, params)
        results = html.xpath('//div[@class="ResultBlock"]//div[@class="ResultCont"]')

        for literature in results:
            item = LiteratureItem()
            item.link = base_url + literature.xpath('.//div[@class="title"]/a/@href')[0]
            item.title = ''.join(literature.xpath('.//div[@class="title"]/a/text()'))
            item.authors = ' '.join(literature.xpath('.//div[@class="author"]/a/text()'))
            item.brief = ''.join(literature.xpath('.//div[@class="summary"]/text()'))
            item.source_name.append('万方')
            item.source_link.append(base_url)

            self.literature_list.append(item)

    def wp_parse(self):
        base_url = 'http://www.cqvip.com'
        url = base_url + '/data/main/search.aspx'
        params = {
            'action': 'so',
            'k': self.keywords,
            'curpage': self.page,
            'prepage': 0,
            '_': int(round(time.time() * 1000))
        }

        results = response(url, params)

    def run(self):
        self.worker(self.SourceType.WF)

        return self.literature_list

    # search source
    class SourceType(Enum):
        WF = 0  # wan fang
        WP = 1 # wei pu


if __name__ == '__main__':
    pass
