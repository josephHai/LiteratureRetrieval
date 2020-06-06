# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy import FormRequest, Request, Selector

from ..utils import get_config
from ..rules import rules
from .. import urls
from ..items import *
from ..loaders import *


class LiteratureSpider(CrawlSpider):
    name = 'literature'
    sql_list = []

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get('start_urls')

        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
        self.allowed_domains = config.get('allowed_domains')
        super(LiteratureSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        start_urls = self.config.get('start_urls')

        if start_urls.get('type') == 'post':
            url = start_urls.get('value')
            headers = start_urls.get('headers')
            data_list = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))

            for data in data_list:
                yield FormRequest(url, headers=headers, formdata=data, callback=self.parse_item, dont_filter=True)
        else:
            for url in self.start_urls:
                yield Request(url, headers=start_urls.get('headers'), callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = self.config.get('item')
        print(response.text)

        if item:
            results = response.xpath(item.get('box_path'))
            for literature in results:
                cls = eval(item.get('class'))()
                loader = eval(item.get('loader'))(cls, selector=literature, crawler='wf')
                for key, value in item.get('attrs').items():
                    for extractor in value:
                        if extractor.get('method') == 'xpath':
                            loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                        if extractor.get('method') == 'css':
                            loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                        if extractor.get('method') == 'value':
                            loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                        if extractor.get('method') == 'attr':
                            loader.add_value(key, getattr(response, *extractor.get('args')))
                yield loader.load_item()
