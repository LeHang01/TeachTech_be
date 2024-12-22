from django.db import models


class Document(models.Model):
    """
    Bảng lưu thông tin tài liệu đính kèm.
    """
    file_url = models.CharField(null=True, blank=True)  # Lưu tệp vào thư mục 'documents/'
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Document {self.id}"
