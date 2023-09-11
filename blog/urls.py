from django.urls import path, re_path

from blog import views


urlpatterns = [
    path('home/', views.home_page, name="home"),
    path('articles/', views.articles_list, name="articles"),
    path('articles/<slug:article_slug>/', views.article_detail, name='article_detail'),
    path('articles/<slug:article_slug>/like/', views.article_like_or_dislike, name='article_like'),
    # re_path(r'^(?P<article>[-\w]+)/$', views.article_detail, name='article_detail'),
]


