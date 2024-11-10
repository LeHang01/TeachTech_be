# payments/views.py

from rest_framework import generics, viewsets, status
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
