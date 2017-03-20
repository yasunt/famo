from django import template
from counsel.models import Question, Answer, Category
from django.contrib.auth.forms import AuthenticationForm

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
            print(Question.objects.order_by('-hits')[:num])
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

@register.inclusion_tag('commons/login_modal.html')
def login_modal():
    return {'login_form': AuthenticationForm()}
