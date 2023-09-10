from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Article, LikeArticle


def home_page(request):
    return render(request, 'home.html', {'title': "Привет?", })


# @login_check()
def articles_list(request):
    articles = Article.objects.filter(status=True)
    return render(request, 'articles_list.html', {'articles': articles})


def article_detail(request, article):
    article = get_object_or_404(Article, slug=article, status=True, )
    return render(request, 'detail.html', {'article': article})


def article_like_or_dislike(request, article):
    if request.method == 'GET':
        if request.GET.get("like"):
            pass
        elif request.GET.get("dislike"):
            pass
    return HttpResponseRedirect('/')
