from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'wf': (
        Rule(LinkExtractor(allow='^$'), callback='parse_item', follow=False),
    ),
    'ixs': (
        Rule(LinkExtractor(allow='^$'), callback='parse_item', follow=False),
    )
}