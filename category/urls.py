from django.conf.urls import url, include
from . import views

app_name = 'category'
urlpatterns = [
    url(r'^topics/$', views.topics, name='topics'),
]
