from django.shortcuts import render

def topics(request, category):
    context = {'category': category}
    return render(request, 'category/topics.html', context)
