from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.apis.teachers import TeacherViewSet

router = DefaultRouter()
router.register('teachers', TeacherViewSet, basename='teachers')

urlpatterns = [
    path('', include(router.urls)),
]