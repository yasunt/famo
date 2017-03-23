from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import FamoUser
from articles.models import Comment
from counsel.models import Answer, Question
from django.db.models import Count
import json

@login_required
def index(request):
    good_points = Answer.objects.filter(user=request.user).aggregate(Count('good_rators'))['good_rators__count'] + Comment.objects.filter(user=request.user).aggregate(Count('good_rators'))['good_rators__count']
    questions_count = Question.objects.filter(user=request.user).count()
    answers_count = Answer.objects.filter(user=request.user).count()
    comments_count = Comment.objects.filter(user=request.user).count()
    context = {'user': request.user, 'good_points': good_points, 'questions_count': questions_count, 'answers_count': answers_count, 'comments_count': comments_count}
    return render(request, 'portfolio/index.html', context)

def user(request, username):
    user = get_object_or_404(FamoUser, username=username)
    context = {'user': user}
    if user in request.user.follows.all():
        context['following'] = True
    else:
        context['following'] = False
    return render(request, 'portfolio/user.html', context)

@login_required
def follow(request):
    if request.method == 'POST':
        user = get_object_or_404(FamoUser, username=request.POST['username'])
        if user in request.user.follows.all():
            request.user.follows.remove(user)
            response = json.dumps({'state': 'フォローする'})
        else:
            request.user.follows.add(user)
            response = json.dumps({'state': 'フォロー中'})
        return HttpResponse(response)
    else:
        pass

def answers(request, username):
    context = {'answers': Answer.objects.filter(user__username=username)}
    return render(request, 'portfolio/answers.html', context)

def comments(request):
    return render(request, 'portfolio/comments.html')

def questions(request):
    return render(request, 'portfolio/question.html')

def test(request):
    return render(request, 'test/index.html')
