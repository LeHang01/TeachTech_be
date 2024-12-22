from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema  # Import decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers.auth import LoginSerializer


class LoginViewSet(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,  # Chỉ định serializer request
        responses={200: "Success", 400: "Bad Request", 500: "Server Error"}  # Các mã trả về
    )
    def post(self, request):
        # Lấy thông tin từ request
        username = request.data.get('username')
        password = request.data.get('password')

        # Kiểm tra xem người dùng có tồn tại và mật khẩu có đúng không
        user = authenticate(username=username, password=password)

        if user is not None:
            first_name = user.first_name
            last_name = user.last_name
            full_name = first_name + ' ' + last_name
            # Nếu xác thực thành công, trả về thông tin người dùng
            return Response({"message": "Đăng nhập thành công", "username": user.username, "user_id": user.id,
                             "is_teacher": user.is_teacher, "full_name": full_name, "id": user.id}, status=status.HTTP_200_OK)
        else:
            # Nếu không thành công, trả về lỗi
            return Response({"message": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)
