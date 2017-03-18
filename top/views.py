from django.shortcuts import render
from articles.models import Article

def index(request):
    context = {'popular_article': Article.objects.order_by('-hits')[0]}
    return render(request, 'top/index.html', context)
