from django import template
from netchan.models import Category

register = template.Library()

@register.inclusion_tag('netchan/category_list.html')
def get_category_list(category=None):
    return {'categories': Category.objects.all(),
            'current_category': category}