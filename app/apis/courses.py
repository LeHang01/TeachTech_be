# app/views.py

from rest_framework import generics, viewsets

from app.models import Course
from app.serializers.courses import CategorySerializer, CourseListSerializer, CourseDetailSerializer


# API cho danh sách khóa học theo danh mục
class CourseViewSet(viewsets.GenericViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView,
                    generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
