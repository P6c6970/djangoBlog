from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from utils.for_account import login_check
from .froms import CommentForm
from .models import Article, LikeArticle, Comment


def home_page(request):
    articles = Article.objects.filter(status=True).annotate(
        likes=Coalesce(Sum("likearticle__like_or_dislike"), 0)).order_by("-likes", )
    return render(request, 'articles_list.html', {'title': "Популярное", 'articles': articles})


# @login_check()
def articles_list(request):
    # articles = Article.objects.filter(status=True)
    articles = Article.objects.filter(status=True).annotate(likes=Coalesce(Sum("likearticle__like_or_dislike"), 0))
    return render(request, 'articles_list.html', {'title': "Последние обновления", 'articles': articles})


@login_check()
def articles_liked_list(request):
    articles = Article.objects.filter(status=True, likearticle__like_or_dislike=1,
                                      likearticle__author=request.user).annotate(
        likes=Coalesce(Sum("likearticle__like_or_dislike"), 0))
    return render(request, 'articles_list.html',
                  {'title': "Понравившиеся", 'null_articles': "У вас еще нет понравившихся статей",
                   'articles': articles})


@method_decorator(login_check(), name='dispatch')
class ArticleForYou(ListView):
    """
    Представление, выводящее список статей авторов, на которые подписан текущий пользователь
    """
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        authors = self.request.user.following.values_list('id', flat=True)
        queryset = self.model.objects.all().filter(author__id__in=authors).annotate(
            likes=Coalesce(Sum("likearticle__like_or_dislike"), 0))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи ваших авторов'
        context['null_articles'] = "У вас еще нет статей этой подборки, подписывайтесь на авторов чтобы исправить это"
        return context


@login_check()
def articles_for_you_list(request):
    articles = Article.objects.filter(status=True, likearticle__author__in=request.user.followers).annotate(
        likes=Coalesce(Sum("likearticle__like_or_dislike"), 0))
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
    comments = Comment.objects.filter(article=get_object_or_404(Article, slug=article_slug, status=True, )).order_by("-date", )
    return render(request, 'detail.html', {'article': article, 'count_like': count_like, 'count_dislike': count_dislike,
                                           'user_like': user_like, 'comment_form': CommentForm, 'comments': comments})


@login_check()
def article_like_or_dislike(request, article_slug):
    """ajax метод для лайков и дизлайков статей"""
    # request.is_ajax() удалили, поэтому request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        like_or_dislike = int(request.POST["like_or_dislike"])
        try:
            like = LikeArticle.objects.get(article__slug=article_slug, author=request.user)
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


@login_check()
def article_add_comment(request, article_slug):
    """ajax метод для лайков и дизлайков статей"""
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(article=get_object_or_404(Article, slug=article_slug, status=True, ),
                              author=request.user,
                              content=form.cleaned_data.get("comment_area"),
                              parent_comment=form.cleaned_data.get("parent_comment")
                              ).save()
            return JsonResponse({}, status=200)
    return JsonResponse({}, status=500)


@login_check()
def article_show_comments(request, article_slug):
    comments = Comment.objects.filter(article=get_object_or_404(Article, slug=article_slug, status=True, )).order_by("-date", )
    return render(request, 'show_comments.html', {'comments': comments})
