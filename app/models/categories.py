# models.py
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Tên danh mục
    description = models.TextField(blank=True, null=True)  # Mô tả danh mục

    def __str__(self):
        return self.name
