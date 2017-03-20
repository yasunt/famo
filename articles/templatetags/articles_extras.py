import os
from django import template
from django.conf import settings
from django.db.models import Count
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
def count_good_rators(comment):
    return comment.good_rators.count()

@register.filter
def top_comment(article):
    if article.comment_set.count() > 0:
        article.comment_set.annotate(rates=Count('good_rators')).order_by('-rates')[0]
    else:
        return ''

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

@register.inclusion_tag('articles/article_detail_button.html')
def article_detail_button(article):
    return {'article': article}

@register.inclusion_tag('articles/article_origin_button.html')
def article_origin_button(article):
    return {'article': article}
