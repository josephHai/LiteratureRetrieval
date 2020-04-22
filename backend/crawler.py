import requests
from lxml import etree
from enum import Enum
from backend.models import *
import time
import re
from pyhanlp import *
import random

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


class Crawler:
    def __init__(self, text, page):
        self.keywords = text
        self.page = page
        self.page_size = 10
        self.literature_map = LiteratureMap()
        self.total_num = 0

        self.handle_kw(allow_pos=['ni', 'nr', 'ns', 'nt', 'ntu', 'nx', 'nz'])

    def handle_kw(self, top=10, allow_pos=None):
        s1 = ''
        for term in HanLP.segment(self.keywords):
            word, pos = term.word, term.nature
            if allow_pos is not None:
                if pos.__str__() in allow_pos:
                    s1 += word
            else:
                s1 += word
        self.keywords = ' '.join(HanLP.extractKeyword(s1, top))

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
        html = self.response(url, params)
        results = html.xpath('//div[@class="ResultBlock"]//div[@class="ResultCont"]')
        self.total_num = html.xpath('//div[@class="BatchOper_result_show"]/span/text()')

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

        results = self.response(url, params)

    def bd_parse(self):
        url = 'http://xueshu.baidu.com/s?wd={}&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_hit=1'.format(self.keywords)

        html = self.response(url)

        results = html.xpath('//div[@class="sc_content"]')
        total_num = html.xpath('//div[@id="toolbar"]//span[@class="nums"]/text()')

        self.total_num = ''.join(re.findall(r'\d', total_num[0])) if len(total_num) else 0

        for literature in results:
            item = Literature()

            item.title = ''.join(literature.xpath('.//h3[contains(@class, "c_font")]/a//text()'))
            item.link = literature.xpath('.//h3[contains(@class, "c_font")]/a/@href')[0]
            item.brief = ''.join(literature.xpath('.//div[@class="c_abstract"]//text()'))
            item.authors = ' '.join(literature.xpath('.//div[@class="sc_info"]/span[1]/a/text()'))
            item.source_name = '|'.join(literature.xpath('.//span[@class="v_item_span"]/a/@title'))
            item.source_link = '|'.join(literature.xpath('.//span[@class="v_item_span"]/a/@href'))

            self.literature_map.append(item)

    def run(self):
        print(self.keywords)
        self.worker(self.SourceType.BD)

        return self.literature_map, self.total_num

    @staticmethod
    def response(url, params=None):
        html = requests.get(url, params=params, headers={'User-Agent': random.choice(USER_AGENT_LIST)}).text
        return etree.HTML(html)

    # search source
    class SourceType(Enum):
        WF = 0  # wan fang
        WP = 1  # wei pu
        BD = 2  # bai du


if __name__ == '__main__':
    pass
