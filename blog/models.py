from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import CustomUser


class Article(models.Model):
    class Meta:
        ordering = ('-date',)

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField("Статус публикации", default=True)
    date = models.DateTimeField("Дата публикации", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField('Комментарий')
    date = models.DateTimeField('Дата комментария', default=timezone.now)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField("Лайк или дизлайк", default=True)

    def __str__(self):
        return self.content[0:200]


class LikeArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CHOICES = (
        (-1, 'Дизлайк'),
        (1, 'Лайк')
    )
    like_or_dislike = models.SmallIntegerField("Лайк или дизлайк", choices=CHOICES)


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CHOICES = (
        (-1, 'Дизлайк'),
        (1, 'Лайк')
    )
    like_or_dislike = models.SmallIntegerField("Лайк или дизлайк", choices=CHOICES)


class Subscribe(models.Model):
    subject = models.ForeignKey(CustomUser, related_name='subjects', on_delete=models.CASCADE)
    object = models.ForeignKey(CustomUser, related_name='objects', on_delete=models.CASCADE)


class TagArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
