import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from articles.models import Article, Comment
from accounts.models import FamoUser


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.hits += 1
    article.save()
    comments = article.comment_set.all()
    context = {'article': article, 'comments': comments}
    return render(request, 'articles/detail.html', context)

def popular(request):
    return render(request, 'articles/popular.html')

@login_required
def comment(request):
    if not request.method == 'POST':
        raise Http404
    else:
        pass
    try:
        article_id = request.POST['article_id']
        content = request.POST['content']
    except:
        raise Http404
    article = get_object_or_404(Article, id=article_id)
    comment = article.comment_set.filter(user=request.user)
    if comment:
        comment = comment[0]
        comment.content = content
    else:
        comment = Comment(user=request.user, content=request.POST['content'], article=article)
    comment.save()
    response = json.dumps({'state': comment.id})
    return HttpResponse(response)
    # return render(request, 'articles/detail.html', {'article': article})

@login_required
def evaluate(request):
    if request.method == 'POST':
        if request.user.id != request.POST['user_id']:
            # raise HTTPERROR
            pass
        comment = get_object_or_404(Comment, id=request.POST['comment_id'])
        if not comment.good_rators.filter(id=request.user.id).exists():
            comment.good_rators.add(request.user)
            response = json.dumps({'good_rators_count': comment.good_rators.count(), 'is_evaluated': True})
        else:
            comment.good_rators.remove(request.user)
            response = json.dumps({'good_rators_count': comment.good_rators.count(), 'is_evaluated': False})
        return HttpResponse(response)
    else:
        pass

def get_last_comment(request):
    if request.method != 'POST':
        raise Http404
    if not request.user.id:
        return HttpResponse(json.dumps({'content': None}))
    try:
        article_id = request.POST['article_id']
    except:
        raise Http404
    article = get_object_or_404(Article, id=article_id)
    user = get_object_or_404(FamoUser, id=request.user.id)
    comment_objs = article.comment_set.filter(user=user)
    if comment_objs.exists():
        return HttpResponse(json.dumps({'content': comment_objs[0].content}))
    else:
        return HttpResponse(json.dumps({'content': None}))
