from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from counsel.scripts import validator
from counsel.models import Question, Answer

@login_required
def post(request):
    title = request.POST['title']
    content = request.POST['content']
    if title and content:
        if validator.is_valid(title) and validator.is_valid(content):
            try:
                question = Question(title=title, content=content, user=request.user)
                question.save()
                context = {'message': 'Posted.'}
            except:
                context = {'message': 'Inappropriate Sentence.'}
        else:
            context = {'message': 'Inappropriate Sentence.'}
    else:
        context = {'message': 'Content is insufficient.'}
    return render(request, 'counsel/post.html', context)

def question(request, question_id):
    context = {'question': Question.objects.get(id=question_id), 'user': request.user}
    return render(request, 'counsel/question.html', context)

@login_required
def delete(request, question_id):
    return render(request, 'counsel/question.html')
