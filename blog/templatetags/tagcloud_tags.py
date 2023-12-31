from django import template
from django.db.models import Count
from taggit.models import Tag

register = template.Library()


@register.simple_tag()
def get_tagcloud():
    return Tag.objects.filter(article__status=True).annotate(count=Count('taggit_taggeditem_items'))
