import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from counsel.scripts import validator
from counsel.models import Question, Answer, Category
from accounts.models import FamoUser

@login_required
def post_question(request):
    return post_content(request, 'question')

@login_required
def post_answer(request):
    return post_content(request, 'answer')

def get_last_answer(request):
    if request.method != 'POST':
        raise Http404
    if not request.user.id:
        return HttpResponse(json.dumps({'content': None}))
    try:
        question_id = request.POST['question_id']
    except:
        raise Http404
    question = get_object_or_404(Question, id=question_id)
    user = get_object_or_404(FamoUser, id=request.user.id)
    answer_objs = question.answer_set.filter(user=user)
    if answer_objs.exists():
        return HttpResponse(json.dumps({'content': answer_objs[0].content}))
    else:
        return HttpResponse(json.dumps({'content': None}))

def popular(request):
    return render(request, 'counsel/popular.html', {'questions': Question.objects.order_by('-hits')[:20]})

def post_content(request, content_type):
    if not request.method == 'POST':
        raise Http404
    content = request.POST['content']
    print(request.POST['anonymous'])
    try:
        anonymous = True if request.POST['anonymous'] == 'true' else False
    except:
        anonymous = False
    if not validator.is_valid(content):
        raise Http404
    if content_type == 'question':
        title = request.POST['title']
        try:
            category = get_object_or_404(Category, id=request.POST['category'])
        except:
            raise Http404   # invalid category.
        try:
            question = Question(title=title, content=content, user=request.user, anonymous=anonymous)
            question.save()
            question.category_set.add(category)
            return HttpResponse(json.dumps({'question_id': question.id}))
        except:
            raise HTTP404   # server error.
    elif content_type == 'answer':
        question = get_object_or_404(Question, id=request.POST['question_id'])
        answer = question.answer_set.filter(user=request.user)
        if answer.exists():
            answer = answer[0]
            answer.content = content
            if anonymous:
                answer.anonymous = True
            else:
                answer.anonymous = False
            answer.save()
        else:
            try:
                answer = Answer(title='', content=content, question=question, user=request.user, anonymous=anonymous)
                answer.save()
            except:
                raise Http404   # server error.
        return HttpResponse(json.dumps({'answer_id': answer.id}))
    else:
        raise Http404

def check_a_post(request):
    # check time before last post.
    # validate a post. (ex. length, words, ...)
    return True

@login_required
def evaluate(request):
    if request.method == 'POST':
        if request.user.id != request.POST['user_id']:
            # raise HTTPERROR
            pass
        answer = get_object_or_404(Answer, id=request.POST['answer_id'])
        if not answer.good_rators.filter(id=request.user.id).exists():
            answer.good_rators.add(request.user)
            response = json.dumps({'good_rators_count': answer.good_rators.count(), 'is_evaluated': True})
        else:
            answer.good_rators.remove(request.user)
            response = json.dumps({'good_rators_count': answer.good_rators.count(), 'is_evaluated': False})
        return HttpResponse(response)
    else:
        pass

@login_required
def post(request):
    context = {'user': request.user, 'categories': Category.objects.all()}
    return render(request, 'counsel/post.html', context)

@login_required
def delete(request, question_id):
    return render(request, 'counsel/question.html')

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.user:
        question.hits += 1
    else:
        question.last_accessed_date = datetime.now()
    question.save()
    context = {
                'question': question,
                'user': request.user,
                'answers': question.answer_set.all()}
    return render(request, 'counsel/detail.html', context)
