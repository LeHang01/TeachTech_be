from django.db import models
from django.contrib.postgres.fields import ArrayField


class Meeting(models.Model):
    """
    Bảng lưu thông tin lớp học online.
    """
    topic = models.CharField(max_length=255, null=True, blank=True)  # Chủ đề cuộc họp
    platform = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    date_time = models.DateTimeField()
    content = models.TextField(null=True, blank=True)  # Nội dung cuộc họp
    status = models.CharField(max_length=50, choices=[
        ("Chưa bắt đầu", "Chưa bắt đầu"),
        ("Đang diễn ra", "Đang diễn ra"),
        ("Đã kết thúc", "Đã kết thúc")
    ])  # Trạng thái
    ROLL_CALL_CHOICES = [
        ("Chưa điểm danh", "Chưa điểm danh"),
        ("Đang điểm danh", "Đang điểm danh"),
        ("Đã điểm danh", "Đã điểm danh"),
    ]
    attachments = ArrayField(models.IntegerField(), blank=True, default=list)  # Danh sách ID của tài liệu
    participants = ArrayField(models.BigIntegerField(), blank=True, default=list)
    has_attended = models.CharField(max_length=20, choices=ROLL_CALL_CHOICES, default="Chưa điểm danh")  # Trạng thái

    def __str__(self):
        return self.topic
