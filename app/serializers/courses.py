# app/serializers.py

from rest_framework import serializers
from app.models import Category, Course, Teacher
from app.serializers.teachers import TeacherSerializer


# Serializer cho danh mục
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'price', 'max_students', 'teacher','time','start_date']

    def to_representation(self, instance: Course):
        data = super().to_representation(instance)

        if instance.teacher:  # Kiểm tra xem có giáo viên không
            # Giáo viên là một ForeignKey, có thể truy cập trực tiếp
            teacher = instance.teacher
            data['teacher'] = {
                'id': teacher.id,
                'name': teacher.name,
                'age': teacher.age,
                'bio': teacher.bio,
                'qualifications': teacher.qualifications,
                'profile_picture': teacher.profile_picture.url if teacher.profile_picture else None,
                'contact_info': teacher.contact_info,
            }
        else:
            data['teacher'] = None  # Nếu không có giáo viên

        return data
class CategorySerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True, source='course_set')  # Liên kết với các khóa học

    class Meta:
        model = Category
        fields = ['id', 'name', 'courses']  # Các trường của Category
        ref_name = "Courses_CategorySerializer"

# Serializer cho chi tiết khóa học
class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()  # Sử dụng TeacherSerializer để có chi tiết giáo viên
    category = CategorySerializer()  # Sử dụng CategorySerializer để có chi tiết danh mục

    class Meta:
        model = Course
        fields = [
            'id', 'course_name', 'description', 'time', 'start_date', 'end_date',
            'price', 'created_at', 'max_students', 'course_image', 'course_video',
            'teacher', 'category'
        ]
