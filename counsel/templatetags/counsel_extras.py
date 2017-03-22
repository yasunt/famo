from django import template
from counsel.models import Answer, Category, Question
from django.db.models import Count
register = template.Library()

@register.filter
def get_answers(question):
    return Answer.objects.filter(question=question).order_by('-updated_date')[:10]

@register.filter
def get_your_answers(user):
    return Answer.objects.filter(user=user).order_by('-updated_date')

"""
@register.filter
def get_top_answer(question):
    return Question.objects.annotate(Count(rates=good_rators)).order_by('-value')[0]
"""

@register.filter
def get_categories(num=20):
    return Category.objects.all()[:num]

@register.filter
def count_good_rators(answer):
    return answer.good_rators.count()

@register.filter
def is_evaluated_answer(answer, user):
    if answer.good_rators.filter(username=user.username).exists():
        return True
    else:
        return False

@register.inclusion_tag('counsel/question_node.html')
def question_node(question, user):
    return {'question': question, 'user': user}

@register.inclusion_tag('counsel/popular_question_node.html')
def popular_question_node(question):
    answers = question.answer_set
    if answers.count() > 0:
        return {'question': question, 'top_comment': answers.annotate(rates=Count('good_rators')).order_by('-rates')[0]}
    else:
        return {'question': question}

@register.inclusion_tag('counsel/answer_node.html')
def answer_node(answer_obj, user):
    return {'answer': answer_obj, 'user': user}

@register.inclusion_tag('counsel/post_answer_form.html')
def post_answer_form():
    return {}

@register.inclusion_tag('counsel/post_question_node.html')
def post_question_form():
    return {}

@register.inclusion_tag('counsel/post_question_modal.html')
def post_question_modal():
    return {}

@register.inclusion_tag('counsel/post_answer_modal.html')
def post_answer_modal(user):
    if user.username:
        return {'user': True}
    else:
        return {'user': False}

"""
@register.simple_tag
def get_question_node(question_obj, context):
    return QuestionNode(question_obj).render(context)

class QuestionNode(template.Node):
    def __init__(self, question_obj):
        self.question_obj = question_obj

    def render(self, context):
        html = ''.join(['<p>NodeTest', self.question_obj.title, '</p>'])
        return template.Template(html).render(context)
"""
