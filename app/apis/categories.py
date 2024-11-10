# app/views.py

from rest_framework import generics, viewsets
from app.models import Category
from app.serializers.categories import CategorySerializer, CategoryListSerializer, CategoryDetailSerializer


class CategoryViewSet(viewsets.GenericViewSet,
                      generics.ListAPIView,
                      generics.RetrieveAPIView,
                      generics.CreateAPIView,
                      generics.DestroyAPIView,
                      generics.UpdateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        # Sử dụng serializer khác nhau dựa trên hành động
        if self.action == 'list':
            return CategoryListSerializer  # Serializer cho danh sách danh mục
        elif self.action == 'retrieve':
            return CategoryDetailSerializer  # Serializer cho chi tiết danh mục
        return CategorySerializer  # Serializer mặc định cho tạo, cập nhật, và xóa
