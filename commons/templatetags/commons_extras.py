from django import template
from counsel.models import Question, Answer, Category

register = template.Library()

@register.filter
def get_latest_questions(num, category=False):
    if not category:
        try:
            return Question.objects.order_by('-date')[:num]
        except:
            return None
    else:
        try:
            return Question.filter(category=category).order_by('-date')[:num]
        except:
            return None

@register.filter
def get_popular_questions(num, category=False):
    if not category:
        try:
            print('test: {0}'.format(Question.objects.order_by('-hits')[:num]))
            return Question.objects.order_by('-hits')[:num]
        except:
            return None
    else:
        try:
            return Question.objects.filter(category=category).order_by('-hit')[:num]
        except:
            return None

@register.filter
def get_categories(num=30):
    return Category.objects.order_by('name')[:num]
