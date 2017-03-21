from django.conf.urls import url, include
from . import views

app_name = 'category'
urlpatterns = [
    url(r'^(?P<category>\w+)/', views.category, name='category'),
]
