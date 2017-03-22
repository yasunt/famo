from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'top'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^policy/', views.policy, name='policy'),
    url(r'^privacy/', views.privacy, name='privacy'),
]
