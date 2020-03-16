from django.db import models
import json
import re

# Create your models here.


# literature model
class LiteratureItem():

    def __init__(self):
        self.link = ''
        self.title = ''
        self.authors = ''
        self.brief = ''
        self.source_name = []
        self.source_link = []
        self.pattern = r'\r|\t|\n'

    def to_dict(self):
        self_dict = {
            'link': re.sub(self.pattern, '', self.link),
            'title': re.sub(self.pattern, '', self.title),
            'authors': re.sub(self.pattern, '', self.authors),
            'brief': self.brief.replace(self.pattern, ''),
            'sources': {'name': self.source_name, 'link': self.source_link}
        }
        return self_dict

    def __eq__(self, other):
        return self.title == other.title


class LiteratureList(list):
    def __init__(self):
        super().__init__()
        self.type = LiteratureItem

    def append(self, item):
        if not isinstance(item, self.type):
            raise TypeError('item is not of type %s' % self.type)
        # check whether there is a duplicate item
        # if not, add current item to the list
        # else, just update the duplicate item's source info
        if item not in self:
            super(LiteratureList, self).append(item)
        else:
            i = self.index(item)
            tmp = self[i]
            tmp.source_name.append(''.join(item.source_name))
            tmp.source_link.append(''.join(item.source_link))
            self[i] = tmp

    # convert obj to json
    def to_json(self):
        self_list = []
        for item in self:
            self_list.append(item.to_dict())
        return json.dumps(self_list, ensure_ascii=False)


if __name__ == '__main__':
    pass
