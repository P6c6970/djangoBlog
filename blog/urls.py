from django.urls import path, re_path

from blog import views


urlpatterns = [
    path('home/', views.home_page, name="home"),
    path('articles/', views.articles_list, name="articles"),
    re_path(r'^(?P<article>[-\w]+)/$', views.article_detail, name='article_detail'),
]


