from django import template
from django.db.models import Sum, Subquery, OuterRef
from django.db.models.functions import Coalesce

from blog.models import LikeComment

register = template.Library()


@register.simple_tag()
def get_reply_comments(comment, user):
    return comment.comment_set.filter().annotate(likes=Coalesce(Sum("likecomment__like_or_dislike"), 0),
                                                 my_like=Coalesce(Subquery(LikeComment.objects.filter(author=user,
                                                                                                      comment=OuterRef(
                                                                                                          'pk')).values(
                                                     'like_or_dislike')), 0))
