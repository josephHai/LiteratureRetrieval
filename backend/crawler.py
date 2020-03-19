import requests
from lxml import etree
from enum import Enum
from backend.models import *
import time
import re


def response(url, params):
    html = requests.get(url, params).text
    return etree.HTML(html)


class Crawler:

    def __init__(self, text, page):
        self.keywords = text
        self.page = page
        self.page_size = 10
        self.literature_map = LiteratureMap()
        self.total_num = 0

    def worker(self, source):
        switch = {
            self.SourceType.WF: self.wf_parse,
            self.SourceType.WP: self.wp_parse,
            self.SourceType.BD: self.bd_parse
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
            item = Literature()
            item.link = base_url + literature.xpath('.//div[@class="title"]/a/@href')[0]
            item.title = ''.join(literature.xpath('.//div[@class="title"]/a/text()'))
            item.authors = ' '.join(literature.xpath('.//div[@class="author"]/a/text()'))
            item.brief = ''.join(literature.xpath('.//div[@class="summary"]/text()'))
            item.source_name = '万方'
            item.source_link = base_url

            self.literature_map.append(item)

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

    def bd_parse(self):
        base_url = 'http://xueshu.baidu.com'
        url = base_url + '/s'
        params = {
            'wd': self.keywords,
            'pn': (self.page - 1) * 10,
            'tn': 'SE_baiduxueshu_c1gjeupa',
            'ie': 'utf-8',
            'sc_hit': 1
        }
        
        html = response(url, params)
        results = html.xpath('//div[@class="sc_content"]')
        total_num = html.xpath('//div[@id="toolbar"]//span[@class="nums"]/text()')
        self.total_num = ''.join(re.findall(r'\d', total_num[0]))

        for literature in results:
            item = Literature()

            item.title = ''.join(literature.xpath('.//h3[contains(@class, "c_font")]/a//text()'))
            item.link = literature.xpath('.//h3[contains(@class, "c_font")]/a/@href')[0]
            item.brief = ''.join(literature.xpath('.//div[@class="c_abstract"]/text()'))
            item.authors = ' '.join(literature.xpath('.//div[@class="sc_info"]/span[1]/a/text()'))
            item.source_name = '|'.join(literature.xpath('.//span[@class="v_item_span"]/a/@title'))
            item.source_link = '|'.join(literature.xpath('.//span[@class="v_item_span"]/a/@href'))

            self.literature_map.append(item)

    def run(self):
        self.worker(self.SourceType.BD)

        return self.literature_map, self.total_num

    # search source
    class SourceType(Enum):
        WF = 0  # wan fang
        WP = 1 # wei pu
        BD = 2 # bai du


if __name__ == '__main__':
    pass
