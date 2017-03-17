from django import template

register = template.Library()

@register.inclusion_tag('articles/comment_form.html')
def comment_form():
    return {}

@register.inclusion_tag('articles/comment_node.html')
def comment_node(comment):
    return {'comment': comment}
