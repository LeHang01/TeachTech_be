from django.db import models

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)                          # Tên giáo viên
    age = models.PositiveIntegerField()                              # Tuổi
    bio = models.TextField(null=True, blank=True)                    # Giới thiệu
    qualifications = models.CharField(max_length=255, null=True, blank=True)  # Bằng cấp
    profile_picture = models.ImageField(upload_to='teachers/images/', null=True, blank=True)  # Hình ảnh
    contact_info = models.CharField(max_length=255, null=True, blank=True)   # Thông tin liên hệ

    def __str__(self):
        return self.name
