from django.conf.urls import url, include
from . import views

app_name = 'articles'
urlpatterns = [
    url(r'^(?P<article_id>\d+)/$', views.detail, name='detail'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^popular/$', views.popular, name='popular'),
]
