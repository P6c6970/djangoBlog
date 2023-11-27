from django.urls import path

from blog import views

urlpatterns = [
    path('home/', views.home_page, name="home"),
    path('search/', views.search, name="search"),
    path('articles/', views.articles_list, name="articles"),
    path('articles/liked/', views.articles_liked_list, name='articles_liked'),
    path('articles/for_you/', views.ArticleForYouListView.as_view(), name='articles_for_you'),
    path('articles/your_following/', views.my_following, name='my_following'),
    path('articles/my/', views.my_articles_list, name='my_articles_list'),

    path('articles/create/', views.ArticleCreateView.as_view(), name='articles_create'),

    path('articles/tags/<str:tag>/', views.ArticleByTagListView.as_view(), name='articles_by_tags'),

    path('articles/<slug:article_slug>/', views.article_detail, name='article_detail'),
    path('articles/<slug:article_slug>/like/', views.article_like_or_dislike, name='article_like'),
    path('articles/<slug:article_slug>/add_comment/', views.article_add_comment, name='article_add_comment'),
    path('articles/<slug:article_slug>/show_comments/', views.article_show_comments, name='show_comment'),
    path('articles/<slug:article_slug>/like_comment/', views.comment_like_or_dislike, name='comment_like'),
    path('articles/<slug:article_slug>/add_complaint/', views.add_complaint, name='add_complaint'),
    # re_path(r'^(?P<article>[-\w]+)/$', views.article_detail, name='article_detail'),
]
