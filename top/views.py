from django.shortcuts import render, render_to_response
from django.template import RequestContext
from accounts.models import FamoUser
from articles.models import Article
from counsel.models import Question
from accounts.forms import RegistrationForm
from django.conf import settings


def index(request):
    categories = [{'name': '育児', 'img_url': 'commons/images/baby.jpg', 'key': 'child'}, {'name': '受験', 'img_url': 'commons/images/study.jpg', 'key': 'study'},
        {'name': '妊娠・出産', 'img_url': 'commons/images/pregnant.jpg', 'key': 'pregnant'}, {'name': '結婚・夫婦生活', 'img_url': 'commons/images/couple.jpg', 'key': 'couple'}
    ]
    keywords = ['引きこもり', '介護', '保育園', '病気', '主夫', '家事', '高齢出産']
    context = {'popular_article': Article.objects.order_by('-hits')[0], 'popular_question': Question.objects.order_by('-hits')[0], 'categories': categories, 'keywords': keywords}
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
