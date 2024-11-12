# apis/zalopay_create.py

import hashlib
import hmac
import json
import random
import time
from datetime import datetime

import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema  # Import decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Payment
from app.serializers.zalopay import ZaloPayCreateOrderRequestSerializer


class ZaloPayCreateOrder(APIView):
    """
    API tạo đơn hàng thanh toán qua ZaloPay.
    """

    @swagger_auto_schema(
        request_body=ZaloPayCreateOrderRequestSerializer,  # Chỉ định serializer request
        responses={200: "Success", 400: "Bad Request", 500: "Server Error"}  # Các mã trả về
    )
    def post(self, request):
        # Lấy dữ liệu paymentId từ body request
        payment_id = request.data.get('paymentId')
        if not payment_id:
            return Response({"error": "paymentId is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy đối tượng Payment từ database
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Lấy thông tin khóa học từ Payment
        course = payment.course
        course_price = course.price
        course_name = course.course_name

        # Cấu hình ZaloPay
        app_id = settings.ZALOPAY_CONFIG["APP_ID"]
        key1 = settings.ZALOPAY_CONFIG["KEY1"]
        endpoint = settings.ZALOPAY_CONFIG["CREATE_ENDPOINT"]

        # Tạo mã giao dịch ngẫu nhiên
        transID = random.randrange(1000000)
        order = {
            "app_id": app_id,
            "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),  # mã giao dịch có định dạng yyMMdd_xxxx
            "app_user":f"{payment_id}",
            "app_time": int(round(time.time() * 1000)),  # miliseconds
            "embed_data": json.dumps({'redirecturl':'http://localhost:3000/registration-success'}),
            "item": json.dumps([{}]),
            "amount": int(course_price),
            "description": "Thanh Toán Khóa Học: " + str(course_name),
            "bank_code": "zalopayapp",
            "callback_url": 'https://93d9-2402-800-6205-55c9-7d86-f93f-f2a5-bbd.ngrok-free.app/api/zalopay/callback/',
        }

        # Tạo MAC (Message Authentication Code) để bảo mật giao dịch
        mac_data = f"{order['app_id']}|{order['app_trans_id']}|{order['app_user']}|{order['amount']}|{order['app_time']}|{order['embed_data']}|{order['item']}"
        order["mac"] = hmac.new(key1.encode(), mac_data.encode(), hashlib.sha256).hexdigest()

        try:
            # Gửi yêu cầu tới API ZaloPay
            response = requests.post(endpoint, json=order)  # Gửi dữ liệu dưới dạng JSON

            # Kiểm tra nếu có lỗi HTTP
            response.raise_for_status()

            # Chuyển đổi dữ liệu trả về thành JSON
            response_data = response.json()
            return Response(response_data)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
