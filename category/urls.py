from django.conf.urls import url, include
from . import views

app_name = 'category'
urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<category>\S+)/', views.category, name='category'),
]
