from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.apis.meetings import MeetingViewSet

router = DefaultRouter()
router.register('meetings', MeetingViewSet, basename='meetings')

urlpatterns = [
    path('', include(router.urls)),
]
