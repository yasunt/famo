from django import template

register = template.Library()

from counsel.models import Answer, Question


@register.filter
def get_questions(user):
    questions = Question.objects.filter(user=user)[:10]
    return questions

def latest_user_objs(model_, user, num):
    return model_.objects.filter(user=user)[:num]

@register.filter
def latest_answers(user, num):
    return latest_user_objs(Answer, user, num)

@register.filter
def latest_questions(user, num):
    return latest_user_objs(Question, user, num)
