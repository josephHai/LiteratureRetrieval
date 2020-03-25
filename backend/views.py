from django.http import HttpResponse
from backend.crawler import Crawler
import json


# Create your views here.


def search(request):
    text = request.GET['kw']
    res, num = Crawler(text, 1).run()
    # Literature.objects.bulk_create(res.values())
    response = json.dumps({'total': num, 'data': res.to_list()}, ensure_ascii=False)
    return HttpResponse(response)
