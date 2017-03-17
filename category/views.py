from django.shortcuts import render

def topics(request):
    return render(request, 'category/topics.html')
