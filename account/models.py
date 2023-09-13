# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import os

from django.urls import reverse


class CustomUser(AbstractUser):
    email = models.EmailField()
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False,
                                       blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/avatar/")

    def get_avatar(self):
        return os.path.basename(self.avatar.path)

    def get_absolute_url(self):
        return reverse('profile', args=[self.id])


class BanIp(models.Model):
    class Meta:
        db_table = "ban_ip"

    ip_address = models.GenericIPAddressField("IP адрес")
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    status = models.BooleanField("Статус блокировки", default=True)

    def __str__(self):
        return self.ip_address
