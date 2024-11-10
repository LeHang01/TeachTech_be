# app/views/teachers.py

from rest_framework import generics, viewsets
from app.models import Teacher
from app.serializers.teachers import TeacherListSerializer, TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(viewsets.GenericViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView,
                     generics.CreateAPIView,
                     generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Teacher.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer  # Serializer cho danh sách giáo viên
        elif self.action == 'retrieve':
            return TeacherDetailSerializer  # Serializer cho chi tiết giáo viên
        return TeacherSerializer  # Serializer cho tạo, cập nhật, và xóa giáo viên
