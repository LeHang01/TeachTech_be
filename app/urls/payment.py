from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.apis.payment import PaymentViewSet

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]