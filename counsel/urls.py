from django.conf.urls import url, include
from . import views

app_name = 'counsel'
urlpatterns = [
    url(r'^post/$', views.post, name='post'),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^evaluate/$', views.evaluate, name='evaluate'),
    url(r'^post_answer/', views.post_answer, name='post_answer'),
    url(r'^post_question/', views.post_question, name='post_question'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^get_last_answer/', views.get_last_answer, name='get_last_answer'),
    url(r'^check_a_post/$', views.check_a_post, name='check_a_post'),
    url(r'^$', views.index, name='index'),
]
