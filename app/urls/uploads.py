from django.urls import path
from app.apis.uploads import ImageUploadView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]
