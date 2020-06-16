import json

from django.http import HttpResponse
from django.db.models import F

from .crawler.run import Worker
from .models import *


def search(request):
    keywords = request.GET.get('kw', '')
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    source = request.GET.get('sources', '["wp", "wf", "ixs"]')
    source = json.loads(source)

    worker = Worker(keywords, source)
    literature, total = worker.get_data(int(page), limit)
    response = json.dumps({'code': 200, 'data': {'total': total, 'items': literature}}, ensure_ascii=False)

    return HttpResponse(response)


def get_source_list(request):
    sources = Source.objects.annotate(en=F('short_name'), value=F('name')).values('en', 'name', 'url')
    response = json.dumps({'code': 200, 'data': list(sources)}, ensure_ascii=False)
    return HttpResponse(response)
