from django.shortcuts import render
from django.http import Http404
from counsel.models import Answer, Question
from articles.models import Article, Comment
from .forms import SearchForm

def index(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST, prefix='search')
        if search_form.is_valid():
            articles = Article.objects.filter(title__contains=search_form.cleaned_data['q']).order_by('-registered_date')
            questions = Question.objects.filter(title__contains=search_form.cleaned_data['q']).order_by('-updated_date')
            return render(request, 'search/index.html', {'articles': articles, 'questions': questions, 'query': search_form.cleaned_data['q']})
    else:
        return render(request, 'top/index.html')
