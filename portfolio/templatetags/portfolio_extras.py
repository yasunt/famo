from django import template

register = template.Library()

from counsel.models import Question


@register.filter
def get_questions(user):
    questions = Question.objects.filter(user=user)[:10]
    return questions
