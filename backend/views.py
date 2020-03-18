from django.http import HttpResponse
from backend.crawler import Crawler
from backend.models import Literature

# Create your views here.


def search(request):
    text = request.GET['text']
    res = Crawler(text, 1).run()
    # Literature.objects.bulk_create(res.values())
    return HttpResponse(res.to_json())
