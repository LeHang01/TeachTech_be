from django.urls import path
from app.apis.notification import NotificationViewSet

urlpatterns = [
    path('notifications/<str:notification_id>/', NotificationViewSet.as_view(), name='get_notification'),
    path('notifications/<str:user_id>/read/<str:notification_id>/', NotificationViewSet.as_view(),
         name='mark_notification_read'),
]
