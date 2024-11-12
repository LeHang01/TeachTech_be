# models.py
from django.db import models

class Payment(models.Model):

    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='payments')  # Liên kết với model Course
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course.course_name}"
