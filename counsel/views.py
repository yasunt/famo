import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from counsel.scripts import validator
from counsel.models import Question, Answer, Category

@login_required
def post_topic(request):
    return post_content(request, 'question')

def post_content(request, type_):
    title = request.POST['title']
    content = request.POST['content']
    print(title, content)
    print(request.POST['category'])
    try:
        category = Category.objects.get(id=request.POST['category'])
    except:
        return render(request, 'counsel/post.html', context)
    if title and content:
        if validator.is_valid(title) and validator.is_valid(content):
            if type_ == 'question':
                try:
                    question = Question(title=title, content=content, user=request.user)
                    question.save()
                    question.category_set.add(category)
                    context = {'message': 'Posted.'}
                except:
                    context = {'message': 'Inappropriate Sentence.'}
            elif type_ == 'answer':
                try:
                    answer = Answer(title=title, content=content, user=request.user)
                    answer.save()
                except:
                    pass
        else:
            context = {'message': 'Inappropriate Sentence.'}
    else:
        context = {'message': 'Content is insufficient.'}
    return render(request, 'counsel/result.html', context)

def check_a_post(request):
    # check time before last post.
    # validate a post. (ex. length, words, ...)
    return True

@login_required
def post_answer(request, question_id):
    context = {'question': Question.objects.get(id=question_id)}
    if check_a_post(request):
        answer = Answer(title=request.POST['title'], content=request.POST['content'], question=Question.objects.get(id=question_id), user=request.user)
        answer.save()
    else:
        pass
    return render(request, 'counsel/detail.html', context)

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
