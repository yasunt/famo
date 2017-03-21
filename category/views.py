from django.shortcuts import render
from django.db.models import Q
from articles.models import Article
from counsel.models import Question

keywords = {'couple': ['夫婦', '結婚'], 'child': ['育児', '子育て', '赤ちゃん', '赤ん坊'], 'study': ['受験', '教育', '塾'],
    'pregnant': ['妊娠', '出産', '妊活', '不妊'],
}

def category(request, category):
    if category in keywords.keys():
        query = Q()
        for key in keywords[category]:
            query = query | Q(title__contains=key)
        articles = Article.objects.filter(query)
        questions = Question.objects.filter(query)
    context = {'category': category, 'articles': articles, 'questions': questions}
    return render(request, 'category/category.html', context)
