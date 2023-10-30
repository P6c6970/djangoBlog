# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import os

from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomUser(AbstractUser):
    email = models.EmailField()
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False,
                                       blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/avatar/")

    def get_avatar(self):
        if not self.avatar:
            return '/media/images/avatar/none.jpg'
        return self.avatar.url

    # method to create a fake table field in read only mode
    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())


    def get_absolute_url(self):
        return reverse('profile', args=[self.id])

    def save(self, *args, **kwargs):
        if self.pk:
            this_record = CustomUser.objects.get(pk=self.pk)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
        super(CustomUser, self).save(*args, **kwargs)


class BanIp(models.Model):
    class Meta:
        db_table = "ban_ip"

    ip_address = models.GenericIPAddressField("IP адрес")
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    status = models.BooleanField("Статус блокировки", default=True)

    def __str__(self):
        return self.ip_address
