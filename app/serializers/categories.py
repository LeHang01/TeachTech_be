# app/serializers/categories.py

from rest_framework import serializers
from app.models import Category


# Serializer cho danh sách danh mục
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Serializer cho chi tiết danh mục
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



    # Serializer cho tạo và cập nhật danh mục
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        ref_name = "Categories_CategorySerializer"
