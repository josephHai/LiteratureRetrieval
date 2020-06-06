from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose
from .utils import get_config


class LiteratureLoader(ItemLoader):
    title_out = Join('')
    authors_out = Join()
    brief_out = Join('')
    website_out = TakeFirst()


class WfLoader(LiteratureLoader):
    source_in = Compose(lambda x: get_config('wf').get('index') + x[0])


class IXSLoader(LiteratureLoader):
    source_in = Compose(lambda x: get_config('ixs').get('index') + x[0])


class WPLoader(LiteratureLoader):
    source_in = Compose(lambda x: get_config('wp').get('index') + x[0])