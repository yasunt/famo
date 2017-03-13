from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {'user': request.user}
    return render(request, 'portfolio/index.html', context)

def test(request):
    return render(request, 'test/question_sample.html')
