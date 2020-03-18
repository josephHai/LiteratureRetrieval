from django.db import models
import json
import re


# literature model
class Literature(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=200)
    title = models.TextField()
    authors = models.TextField()
    brief = models.TextField()
    source_name = models.CharField(max_length=100)
    source_link = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


class LiteratureMap(dict):
    def __init__(self):
        super().__init__()
        self.type = Literature

    def append(self, item):
        # check whether there is a duplicate item
        # if not, add current item to the list
        # else, just update the duplicate item's source info
        if not isinstance(item, self.type):
            raise TypeError('item is not of type %s' % self.type)
        if self.get(item.title):
            tmp = self[item.title]
            tmp.source_name += '|' + item.source_name
            tmp.source_link += '|' + item.source_link
            self[item.title] = tmp
        else:
            self[item.title] = item

    def to_json(self):
        self_list = []
        for item in self.values():
            self_list.append(item.to_dict())
        return json.dumps(self_list, ensure_ascii=False)


if __name__ == '__main__':
    pass
