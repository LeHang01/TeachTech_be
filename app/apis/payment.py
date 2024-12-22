# payments/views.py

from datetime import datetime

from django.conf import settings
from pymongo import MongoClient
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from unidecode import unidecode

from app.models.payment import Payment
from app.serializers.payments import PaymentSerializer
from app.task import send_notification_batch


class PaymentViewSet(viewsets.GenericViewSet,
                     generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Nhận dữ liệu thanh toán từ frontend
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Lưu bản ghi thanh toán vào cơ sở dữ liệu
        serializer.save()

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
            user_id = user.id
            full_name = user.payment.full_name
            birth_date = user.payment.birth_date
            password = self.generate_password(full_name, birth_date)
            return Response({
                'user_id': user_id,
                'username': username,
                'password': password,
            })

        except Payment.DoesNotExist:
            raise NotFound(detail="Không tìm thấy thanh toán với paymentId này.")

    def generate_password(self, full_name, birth_date):
        full_name_unsigned = unidecode(full_name.strip().lower())

        # Tách từng từ trong tên và lấy ký tự đầu tiên của mỗi từ
        initials = "".join(word[0] for word in full_name_unsigned.split() if word)

        # Lấy ngày tháng năm từ birth_date
        date_str = birth_date.strftime('%d%m%y')  # 2 số ngày, 2 số tháng, 2 số cuối năm

        # Tạo mật khẩu
        password = f"{initials}_{date_str}"
        return password