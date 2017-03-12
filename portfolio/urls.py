from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name= 'portfolio'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
]
