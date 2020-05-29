import json

from django.http import HttpResponse

from .crawler.run import Worker


def search(request):
    keywords = request.GET.get('kw', '')
    page = request.GET.get('page', 1)
    # res, num = Crawler(keywords, page).run()
    # Literature.objects.bulk_create(res.values())
    worker = Worker(keywords)

    response = json.dumps({'code': 200, 'data': {'total': 0, 'items': worker.get_data(int(page), 10)}}, ensure_ascii=False)
    return HttpResponse(response)
