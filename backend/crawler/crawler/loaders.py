from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class LiteratureLoader(ItemLoader):
    pass


class WfLoader(LiteratureLoader):
    authors_out = Compose(Join())
    # title_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
