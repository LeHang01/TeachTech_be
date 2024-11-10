from django.contrib import admin
from django.utils.html import format_html

from app.models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_teacher_image', 'age', 'bio', 'qualifications', 'contact_info')  # Thêm các trường bạn muốn hiển thị
    search_fields = ('name', 'qualifications')  # Cho phép tìm kiếm theo tên và bằng cấp
    list_filter = ('age', 'qualifications')     # Lọc theo tuổi và bằng cấp

    def display_teacher_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.profile_picture.url)
        return "No Image"

    display_teacher_image.short_description = 'Course Image'  # Set column name in admin

