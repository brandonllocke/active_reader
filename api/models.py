from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, null=False, unique=True)
    active = models.BooleanField(default=True, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    pass


class Reading(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
