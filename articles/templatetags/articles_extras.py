import os
from django import template
from django.conf import settings
from articles.models import Article

register = template.Library()

@register.filter
def popular_articles(self, num, category=None):
    if category:
        return Article.objects.order_by('hits')[:num] # filter by categories.
    else:
        return Article.objects.order_by('hits')[:num]

@register.filter
def get_article_image(url):
    default_image_path = 'commons/images/pic01.jpg'
    if url:
        return url
    else:
        return os.path.join(settings.STATIC_URL, default_image_path)

@register.filter
def complete_url(url):
    return ''.join(['http://', url])

@register.inclusion_tag('articles/comment_form.html')
def comment_form():
    return {}

@register.inclusion_tag('articles/comment_node.html')
def comment_node(comment):
    return {'comment': comment}

@register.inclusion_tag('articles/article_node.html')
def article_node(article):
    return {'article': article}
