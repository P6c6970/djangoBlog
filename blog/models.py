from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

from account.models import CustomUser


class Article(models.Model):
    class Meta:
        ordering = ('-date',)

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    short_description = models.TextField("Краткое описание", max_length=200)
    content = CKEditor5Field(verbose_name='Содержание', config_name='extends', blank=True, null=True)
    tags = TaggableManager(blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField("Статус публикации", default=False)
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
    is_active = models.BooleanField("Статус", default=True)

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

    def __str__(self):
        return self.article.title


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CHOICES = (
        (-1, 'Дизлайк'),
        (1, 'Лайк')
    )
    like_or_dislike = models.SmallIntegerField("Лайк или дизлайк", choices=CHOICES)


class ComplaintArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CHOICES = (
        ('1', 'Спам'),
        ('2', 'Запрещенный контент'),
        ('3', 'Обман'),
        ('4', 'Насилие и вражда'),
    )
    type_complaint = models.SmallIntegerField("Тип жалобы", choices=CHOICES)
    STATUS_CHOICES = (
        ('pending', 'В рассмотрении'),
        ('satisfied', 'Удовлетворена'),
        ('rejected', 'Отклонена'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
