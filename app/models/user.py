from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    payment = models.OneToOneField("Payment", on_delete=models.CASCADE,
                                related_name='user',null=True,blank=True)  # Thêm khóa ngoại OneToOne với User
    embedding = models.JSONField(blank=True, null=True)
    is_teacher = models.BooleanField(default=False)  # Boolean field to determine if the user is a teacher
    teacher = models.OneToOneField("Teacher", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='user_teacher')  # Nullable FK to Teacher

    class Meta:
        db_table = 'app_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'