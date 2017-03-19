from django.shortcuts import render, render_to_response
from django.template import RequestContext
from accounts.models import FamoUser
from articles.models import Article
from accounts.forms import RegistrationForm

def index(request):
    context = {'popular_article': Article.objects.order_by('-hits')[0]}
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
