from django.shortcuts import render
from django.db.models import Q
from articles.models import Article
from counsel.models import Question

keywords = {'結婚・夫婦生活': ['夫婦', '結婚', '新婚', 'セックスレス', '新婚'], '育児・子育て': ['育児', '子育て', '赤ちゃん', '赤ん坊', '子ども', '子供', '息子', '娘','ベビー'],
    '教育・習い事': ['受験', '教育', '塾', '習い事', '習いごと'], '妊娠・出産': ['妊娠', '出産', '妊活', '妊婦', '不妊', 'マタニティ', 'ベビー'], '引きこもり': ['引きこもり', 'ひきこもり', 'ニート'],
    '介護': ['介護'], '主夫': ['主夫'],'高齢出産': ['高齢出産'], '習い事': ['習い事', '習いごと'], '保育園': ['保育園', '幼稚園', '待機児童'], '病気': ['病気'],
    '家事': ['家事'],
}

def category(request, category):
    if category in keywords.keys():
        query = Q()
        for key in keywords[category]:
            query = query | Q(title__contains=key)
        articles = Article.objects.filter(query).order_by('-hits')[:15]
        questions = Question.objects.filter(query).order_by('-hits')[:15]
    context = {'category': category, 'articles': articles, 'questions': questions}
    return render(request, 'category/category.html', context)

def list(request):
    return render(request, 'category/list.html', {'keywords': keywords})
