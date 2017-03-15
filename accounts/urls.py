from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
]
