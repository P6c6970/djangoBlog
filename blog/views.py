from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from utils.for_account import login_check
from .models import Article, LikeArticle


def home_page(request):
    articles = Article.objects.filter(status=True).annotate(likes=Coalesce(Sum("likearticle__like_or_dislike"), 0)).order_by("-likes", )
    return render(request, 'home.html', {'articles': articles})


# @login_check()
def articles_list(request):
    # articles = Article.objects.filter(status=True)
    articles = Article.objects.filter(status=True).annotate(likes=Coalesce(Sum("likearticle__like_or_dislike"), 0))
    return render(request, 'articles_list.html', {'articles': articles})


def count_like_and_dislike(article_slug):
    count_like = len(LikeArticle.objects.filter(article__slug=article_slug, like_or_dislike=1))
    if count_like > 999:
        count_like = f"{count_like // 1000} тыс."
    count_dislike = len(LikeArticle.objects.filter(article__slug=article_slug, like_or_dislike=-1))
    if count_dislike > 999:
        count_dislike = f"{count_dislike // 1000} тыс."
    return count_like, count_dislike


@login_check()
def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug, status=True, )
    count_like, count_dislike = count_like_and_dislike(article_slug)
    user_like = LikeArticle.objects.filter(article=article, author=request.user).first()
    if user_like is not None:
        user_like = user_like.like_or_dislike
    return render(request, 'detail.html', {'article': article, 'count_like': count_like, 'count_dislike': count_dislike,
                                           'user_like': user_like})


@login_check()
def article_like_or_dislike(request, article_slug):
    # request.is_ajax() удалили, поэтому request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        like_or_dislike = int(request.POST["like_or_dislike"])
        try:
            like = LikeArticle.objects.get(article__slug=article_slug, author=request.user)
            print(like.like_or_dislike)
            print(like_or_dislike)
            if like.like_or_dislike == like_or_dislike:
                like.delete()
            else:
                like.like_or_dislike = like_or_dislike
                like.save()
        except LikeArticle.DoesNotExist:
            like = LikeArticle(article=get_object_or_404(Article, slug=article_slug, status=True, ),
                               author=request.user, like_or_dislike=like_or_dislike)
            like.save()

    count_like, count_dislike = count_like_and_dislike(article_slug)
    return JsonResponse({'count_like': count_like, 'count_dislike': count_dislike}, status=200)
