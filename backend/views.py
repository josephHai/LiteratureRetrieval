from django.http import HttpResponse
from backend.crawler import Crawler

# Create your views here.


def search(request):
    text = request.GET['text']
    res = Crawler(text, 1).run()

    return HttpResponse(res.to_json())
