from django.shortcuts import render
from accounts.models import FamoUser
from django.http import HttpResponseRedirect

def exists(model, attr, value):
    try:
        model.objects.get(attr=value)
        return True
    except:
        return False

def signup(request):
    if request.method == 'POST':
        if exists(FamoUser, 'username', request.POST['username']):
            pass    # and verify email address.
        else:
            try:
                user = FamoUser.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.save()
                print(request.GET['next'])
                return HttpResponseRedirect(request.GET['next'])
            except:
                pass    # exceptional operation.
    else:
        return render(request, 'registration/signup.html')
    return HttpResponseRedirect(request.GET['next'])
