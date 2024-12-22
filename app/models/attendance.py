from django.conf import settings  # Import model User nếu đang dùng mặc định
from django.db import models


class Attendance(models.Model):
    """
    Bảng lưu thông tin điểm danh.
    """
    STATUS_CHOICES = [
        ("Chưa tham gia", "Chưa tham gia"),
        ("Đã tham gia", "Đã tham gia"),
        ("Vắng", "Vắng"),
    ]

    ABSENCE_REASON_CHOICES = [
        ("Chính đáng", "Chính đáng"),
        ("Không chính đáng", "Không chính đáng"),
    ]

    # Các trường dữ liệu
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="attendances")  # Liên kết đến User
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE, related_name="attendances")  # Liên kết đến Meeting
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Chưa tham gia")  # Trạng thái
    check_in = models.DateTimeField(null=True, blank=True)  # Thời gian check-in
    absence_reason_type = models.CharField(max_length=20, choices=ABSENCE_REASON_CHOICES, null=True,
                                           blank=True)  # Loại lý do vắng
    notes = models.TextField(null=True, blank=True)  # Ghi chú
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    updated_at = models.DateTimeField(auto_now=True)  # Ngày cập nhật

    def __str__(self):
        return f"Attendance: {self.user} - {self.meeting}"
