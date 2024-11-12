# payments/views.py

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.models.payment import Payment
from app.serializers.payments import PaymentSerializer


class PaymentViewSet(viewsets.GenericViewSet,
                     generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Nhận dữ liệu thanh toán từ frontend
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Lưu bản ghi thanh toán vào cơ sở dữ liệu
        payment = serializer.save()

        # Trả về thông tin thanh toán đã lưu
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def user_info(self, request, pk=None):
        """
        Lấy thông tin người dùng liên kết với paymentId.
        """
        try:
            # Lấy đối tượng Payment dựa trên paymentId (pk)
            payment = self.get_object()

            # Kiểm tra xem payment có liên kết với user hay không
            if not payment.user:
                raise NotFound(detail="Không tìm thấy người dùng liên kết với payment này.")

            # Lấy thông tin người dùng
            user = payment.user
            username = user.username
            full_name = user.payment.full_name
            birth_date = user.payment.birth_date
            password = self.generate_password(full_name, birth_date)
            return Response({
                'username': username,
                'password': password,
            })

        except Payment.DoesNotExist:
            raise NotFound(detail="Không tìm thấy thanh toán với paymentId này.")

    def generate_password(self, full_name, birth_date):
        """Generate a password by combining full name and birth date"""
        # Chúng ta có thể kết hợp `full_name` và `birth_date` để tạo mật khẩu
        birth_date_str = birth_date.strftime('%Y%m%d')  # Đổi đối tượng datetime.date thành chuỗi "YYYYMMDD"
        password = f"{full_name.replace(' ', '')}{birth_date_str}"  # Kết hợp full_name (bỏ dấu cách) và birth_date
        return password  # Trả về mật khẩu đã tạo