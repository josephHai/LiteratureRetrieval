# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy import FormRequest, Request

from ..utils import get_config
from ..rules import rules
from .. import urls
from ..items import *
from ..loaders import *


class LiteratureSpider(CrawlSpider):
    name = 'literature'
    param_list = []

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get('start_urls')
        self.parse = self.parse_item
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
            data_list = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
            for data in data_list:
                yield FormRequest(url, method='POST', formdata=data, callback=self.parse_item, dont_filter=True)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)

    def parse_item(self, response):
        name = self.config.get('name')
        website = self.config.get('website')
        base_url = self.config.get('index')

        if name == 'wf':
            results = response.xpath('//div[@class="ResultBlock"]//div[@class="ResultCont"]')

            for literature in results:
                item = LiteratureItem()

                item['title'] = ''.join(literature.xpath('.//div[@class="title"]/a[1]//text()').extract())
                item['authors'] = ' '.join(literature.xpath('.//div[@class="author"]/a/text()').extract())
                item['brief'] = ''.join(literature.xpath('.//div[@class="summary"]//text()').extract())
                item['source'] = base_url + literature.xpath('.//div[@class="title"]/a[1]/@href').extract_first()
                item['website'] = website

                yield item

        if name == 'ixs':
            results = response.xpath('//div[@class="cont-bd"]/ul[contains(@class, "doc-list")]//li')

            for literature in results:
                item = LiteratureItem()

                item['title'] = ''.join(literature.xpath('.//h3/a//text()').extract())
                item['authors'] = ' '.join(literature.xpath('.//div[@class="field"]//span[2]//text()').extract())
                item['brief'] = ''.join(literature.xpath('.//div[@class="intro"]//text()').extract())
                item['source'] = literature.xpath('.//h3/a/@href').extract_first()
                item['website'] = website

                yield item
