from django.shortcuts import render, render_to_response
from django.template import RequestContext
from accounts.models import FamoUser
from articles.models import Article
from counsel.models import Question
from accounts.forms import RegistrationForm
from django.conf import settings
from datetime import datetime

def index(request):
    categories = [{'name': '育児・子育て', 'img_url': 'commons/images/baby.jpg', 'key': 'child'}, {'name': '教育・習い事', 'img_url': 'commons/images/study.jpg', 'key': 'study'},
        {'name': '妊娠・出産', 'img_url': 'commons/images/pregnant.jpg', 'key': 'pregnant'}, {'name': '結婚・夫婦生活', 'img_url': 'commons/images/couple02.jpg', 'key': 'couple'}
    ]
    keywords = ['引きこもり', '介護', '保育園', '病気', '主夫', '家事', '高齢出産']
    today_questions = Question.objects.filter(updated_date__date=datetime.today())
    popular_question = today_questions.order_by('-hits')[0] if today_questions.count() > 0 else Question.objects.order_by('-hits')[0]
    today_articles = Article.objects.filter(registered_date__date=datetime.today())
    popular_article = today_articles.order_by('-hits')[0] if today_articles.count() > 0 else Article.objects.order_by('-hits')[0]
    context = {'popular_article': popular_article, 'popular_question': popular_question, 'categories': categories, 'keywords': keywords}
    return render(request, 'top/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = FamoUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return render(request, 'top/result.html')
        else:
            return render(request, 'top/signup.html', {'error_message': '項目を正しく入力してください'})
    form = RegistrationForm()
    return render(request, 'top/signup.html', {'form': form})

def policy(request):
    return render(request, 'top/policy.html')

def privacy(request):
    return render(request, 'top/privacy.html')
