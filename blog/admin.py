from django.contrib import admin
from .models import Article, Comment, LikeArticle, LikeComment, Subscribe, TagArticle


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'content')


admin.site.register(Comment, CommentAdmin)

admin.site.register(LikeArticle)
admin.site.register(LikeComment)
admin.site.register(Subscribe)
admin.site.register(TagArticle)
