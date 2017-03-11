from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'counsel'
urlpatterns = [
    url(r'^post/$', views.post, name='post'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^delete/(?P<question_id>\d+)/$', views.question, name='delete'),
]
