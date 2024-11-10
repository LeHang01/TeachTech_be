# app/serializers/teachers.py

from rest_framework import serializers
from app.models import Teacher


# Serializer cho danh sách giáo viên
class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'profile_picture', 'qualifications']


# Serializer cho chi tiết giáo viên
class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


# Serializer cho tạo và cập nhật giáo viên
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'age', 'bio', 'qualifications', 'profile_picture', 'contact_info']
