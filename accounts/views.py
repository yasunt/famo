from django.shortcuts import render
from accounts.models import FamoUser

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
            except:
                pass    # exceptional operation.
    else:
        return render(request, 'registration/signup.html')
    return render(request, 'registration/login.html')
