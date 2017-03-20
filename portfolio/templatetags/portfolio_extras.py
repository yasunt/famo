from django import template
from datetime import datetime
from counsel.models import Answer, Question

register = template.Library()


@register.filter
def get_questions(user):
    questions = Question.objects.filter(user=user)[:10]
    return questions

@register.filter
def cut_text(text, num):
    return text[:num]

def latest_user_objs(model_, user, num):
    return model_.objects.filter(user=user)[:num]

@register.filter
def latest_answers(user, num):
    return latest_user_objs(Answer, user, num)

@register.filter
def latest_questions(user, num):
    return latest_user_objs(Question, user, num)

@register.filter
def count_new_answers(question):
    new_answers = question.answer_set.filter(updated_date__gte=question.last_accessed_date)
    if not new_answers:
        return 0
    else:
        return answers.count()

@register.inclusion_tag('portfolio/answer_portfolio_node.html')
def answer_portfolio_node(answer):
    return {'answer': answer}
