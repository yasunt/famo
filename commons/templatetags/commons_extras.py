from django import template
from counsel.models import Question, Answer, Category
from django.contrib.auth.forms import AuthenticationForm
from search.forms import SearchForm

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
def cut_text(text, num):
    if len(text) > num:
        return ''.join([text[:num], '...'])
    else:
        return text

@register.filter
def get_categories(num=30):
    return Category.objects.order_by('name')[:num]

@register.inclusion_tag('commons/login_modal.html')
def login_modal():
    return {'login_form': AuthenticationForm()}

@register.inclusion_tag('commons/search_form.html')
def search_form():
    search_form = SearchForm(prefix='search')
    return {'search_form': search_form}

@register.inclusion_tag('commons/modal_libraries.html')
def modal_libraries():
    return {}
