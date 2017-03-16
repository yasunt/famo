import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from counsel.scripts import validator
from counsel.models import Question, Answer, Category

@login_required
def post_question(request):
    return post_content(request, 'question')

@login_required
def post_answer(request, question_id):
    return post_content(request, 'answer', question_id)

def post_content(request, content_type, question_id=None):
    if not request.method == 'POST':
        raise Http404
    title = request.POST['title']
    content = request.POST['content']
    try:
        anonymous = True if request.POST['anonymous'] == 'true' else False
    except:
        anonymous = False
    print(anonymous)
    if not (validator.is_valid(title) and validator.is_valid(content)):
        context = {'message': 'Inappropriate Sentence.'}
        raise Http404
    else:
        pass
    if content_type == 'question':
        try:
            category = get_object_or_404(Category, id=request.POST['category'])
        except:
            raise Http404   # invalid category.
        try:
            question = Question(title=title, content=content, user=request.user, anonymous=anonymous)
            question.save()
            question.category_set.add(category)
            return render(request, 'counsel/detail.html', {'question': question})
        except:
            raise HTTP404   # server error.
    elif content_type == 'answer':
        question = get_object_or_404(Question, id=question_id)
        try:
            answer = Answer(title=title, content=content, question=question, user=request.user, anonymous=anonymous)
            answer.save()
            return render(request, 'counsel/detail.html', {'question': question})
        except:
            raise Http404   # server error.
    else:
        raise Http404

def check_a_post(request):
    # check time before last post.
    # validate a post. (ex. length, words, ...)
    return True

@login_required
def evaluate(request):
    print(type(request.POST['answer_id']))
    if request.method == 'POST':
        if request.user.id != request.POST['user_id']:
            # raise HTTPERROR
            pass
        answer = get_object_or_404(Answer, id=request.POST['answer_id'])
        print(answer)
        if not answer.good_rators.filter(id=request.user.id).exists():
            answer.good_rators.add(request.user)
        response = json.dumps({'good_rators_count': answer.good_rators.count()})
        return HttpResponse(response)
    else:
        pass

@login_required
def post(request):
    context = {'user': request.user, 'categories': Category.objects.all()}
    return render(request, 'counsel/post.html', context)

def question(request, question_id):
    context = {'question': Question.objects.get(id=question_id), 'user': request.user}
    return render(request, 'counsel/question.html', context)

@login_required
def delete(request, question_id):
    return render(request, 'counsel/question.html')

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {
                'question': question,
                'user': request.user,
                'answers': question.answer_set.all()}
    return render(request, 'counsel/detail.html', context)
