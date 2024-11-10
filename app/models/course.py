from django.db import models
from .teachers import Teacher
from .categories import Category



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    time = models.TimeField()  # New field to store time in hh:mm format
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)  # Sử dụng khóa ngoại đến Teacher
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name="courses")  # Khóa ngoại tới Category
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    max_students = models.IntegerField()
    course_image = models.ImageField(upload_to='courses/images/', null=True, blank=True)
    course_video = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.course_name


