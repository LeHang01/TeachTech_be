from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.apis.face import FaceViewSet

router = DefaultRouter()
router.register('faces', FaceViewSet, basename='faces')

urlpatterns = [
    path('', include(router.urls)),
]