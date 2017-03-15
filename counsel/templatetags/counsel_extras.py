from django import template
from counsel.models import Answer, Category

register = template.Library()

@register.filter
def get_answers(question):
    return Answer.objects.filter(question=question).order_by('date')[:10]

@register.filter
def get_categories(num=20):
    return Category.objects.all()[:num]

@register.filter
def count_good_rators(answer):
    return answer.good_rators.count()

@register.inclusion_tag('counsel/node.html')
def get_question_node(question_obj, user):
    return {'question': question_obj, 'user': user}

@register.inclusion_tag('counsel/node.html')
def get_answer_node(answer_obj, user):
    return {'answer': answer_obj, 'user': user}

@register.inclusion_tag('counsel/post_answer_node.html')
def post_form(question_id):
    return {'question_id': question_id}
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
