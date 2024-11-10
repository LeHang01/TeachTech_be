from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    embedding = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'app_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'