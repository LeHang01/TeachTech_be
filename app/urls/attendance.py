from django.urls import include, path
from rest_framework.routers import DefaultRouter
from app.apis.attendance import AttendanceViewSet

router = DefaultRouter()
router.register('attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('attendance/<int:meeting_id>/', AttendanceViewSet.as_view({'get': 'list'}), name='attendance-list'),
]
