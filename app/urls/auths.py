from django.urls import path

from app.apis.auths import LoginViewSet

urlpatterns = [
    path('auth/login/', LoginViewSet.as_view(), name='auth_login'),
]
