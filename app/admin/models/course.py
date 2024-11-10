from django.contrib import admin
from django.utils.html import format_html
from app.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'course_name', 'display_course_image',
    'display_course_video', 'max_students', 'price', 'teacher','time')
    search_fields = ('course_name', 'description')
    list_filter = ('start_date', 'end_date')

    def display_course_image(self, obj):
        if obj.course_image:
            return format_html('<img src="{}" style="height: 113px; width: 200px;" />', obj.course_image.url)
        return "No Image"

    display_course_image.short_description = 'Course Image'  # Set column name in admin

    def display_course_video(self, obj):
        if obj.course_video:
            video_id = obj.course_video.split("v=")[-1]  # Extract video ID from the URL
            return format_html(
                '<iframe width="200" height="113" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
                video_id
            )
        return ""

    display_course_video.short_description = 'Course Video'

