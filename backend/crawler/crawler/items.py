# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiteratureItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    brief = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()
    pass
