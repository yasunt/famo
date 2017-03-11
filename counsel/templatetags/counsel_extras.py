from django import template
from counsel.models import Answer

register = template.Library()

@register.filter
def get_answers(question):
    return Answer.objects.filter(question=question).order_by('-value')[:10]
