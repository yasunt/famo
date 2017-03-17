import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from articles.models import Article, Comment


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comment_set.all()
    context = {'article': article, 'comments': comments}
    return render(request, 'articles/detail.html', context)

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
    comment = article.comment_set.filter(user=request.user)[0]
    if comment:
        comment.content = content
    else:
        comment = Comment(user=request.user, content=request.POST['content'], article=article)
    comment.save()
    response = json.dumps({'state': comment.id})
    return HttpResponse(response)
    # return render(request, 'articles/detail.html', {'article': article})
