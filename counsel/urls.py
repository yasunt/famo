from django.conf.urls import url, include
from . import views

app_name = 'counsel'
urlpatterns = [
    url(r'^post/$', views.post, name='post'),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^evaluate/$', views.evaluate, name='evaluate'),
    url(r'^post_answer/(?P<question_id>\d+)/$', views.post_answer, name='post_answer'),
    url(r'^post_question/$', views.post_question, name='post_question'),
    url(r'^detail/(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^delete/(?P<question_id>\d+)/$', views.question, name='delete'),
    url(r'^check_a_post/$', views.check_a_post, name='check_a_post'),
]
