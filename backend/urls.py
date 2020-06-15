from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search', views.search),
    url(r'^getSource', views.get_source_list)
]
