from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import FamoUser
import json

@login_required
def index(request):
    context = {'user': request.user}
    return render(request, 'portfolio/index.html', context)

@login_required
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

def test(request):
    return render(request, 'test/index.html')
