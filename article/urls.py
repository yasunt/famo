from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^detail/(?P<article_id>\d+)/$', views.detail, name='detail'),
]
