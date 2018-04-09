from django import template
from django.db.models.aggregates import Count

from ..models import Category, Tag, Article, MyAuthor

register = template.Library()


@register.simple_tag
def get_category():
    return Category.objects.annotate(num_articlies=Count('article'))


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def archives():
    return Article.objects.dates('add_date', 'month', order='DESC')


@register.simple_tag
def get_author_info():
    return MyAuthor.objects.first()

