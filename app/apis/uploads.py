import os

from django.conf import settings
from django.core.files.storage import default_storage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Upload multiple images",
        manual_parameters=[
            openapi.Parameter(
                name="images",
                in_=openapi.IN_FORM,
                description="List of images to upload",
                type=openapi.TYPE_FILE,
                required=True,
                multiple=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Upload successful",
                examples={"application/json": {"message": "Images uploaded successfully", "files": ["url1", "url2"]}},
            ),
        },
    )
    def post(self, request):
        images = request.FILES.getlist('images')
        saved_files = []

        # Đường dẫn thư mục 'uploads'
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(upload_dir, exist_ok=True)

        for img in images:
            file_path = os.path.join(upload_dir, img.name)

            # Lưu file
            with default_storage.open(file_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)

            # Thêm đường dẫn file vào danh sách trả về
            saved_files.append(os.path.join(settings.MEDIA_URL, 'uploads', img.name))

        return Response({"message": "Images uploaded successfully", "files": saved_files})
