# apis/zalopay_create.py

import hmac
import hashlib
import json
import time
import random
from datetime import datetime

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests

from app.models import Payment
from app.serializers.payments import PaymentZalo
from app.serializers.zalopay import ZaloPayOrderSerializer


class ZaloPayCreateOrder(APIView):
    """
    API tạo đơn hàng thanh toán qua ZaloPay.
    """

    def post(self, request):
        print('abccc',request.data)
        payment_id = request.data.get('paymentId')
        payment = Payment.objects.get(id=payment_id)
        # Lấy Course từ Payment
        course = payment.course

        # Lấy giá trị price từ Course
        course_price = course.price
        course_name = course.course_name
        app_id = settings.ZALOPAY_CONFIG["APP_ID"]
        key1 = settings.ZALOPAY_CONFIG["KEY1"]
        endpoint = settings.ZALOPAY_CONFIG["CREATE_ENDPOINT"]
        print(course_price)
        print(course_name)

        # Tạo mã giao dịch ngẫu nhiên
        transID = random.randrange(1000000)
        order = {
            "app_id": app_id,
            "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),  # mã giao dich có định dạng yyMMdd_xxxx
            "app_user": "user123",
            "app_time": int(round(time.time() * 1000)),  # miliseconds
            "embed_data": json.dumps({}),
            "item": json.dumps([{}]),
            "amount": int(course_price),
            "description": "Thanh Toán Khóa Học:" + str(course_name),
            "bank_code": "zalopayapp",
            "callback_url": 'https://9c06-2402-800-6205-b50a-7c4a-8a16-cfde-47e9.ngrok-free.app/',
        }

        # Tạo MAC (Message Authentication Code)
        mac_data = f"{order['app_id']}|{order['app_trans_id']}|{order['app_user']}|{order['amount']}|{order['app_time']}|{order['embed_data']}|{order['item']}"
        order["mac"] = hmac.new(key1.encode(), mac_data.encode(), hashlib.sha256).hexdigest()

        try:
            # Gửi yêu cầu tới API ZaloPay
            response = requests.post(endpoint, data=order)

            # Kiểm tra nếu có lỗi HTTP
            response.raise_for_status()

            # Chuyển đổi dữ liệu trả về thành JSON
            try:
                response_data = response.json()
                print(response_data)
            except ValueError:
                return Response({"error": "Invalid JSON response from ZaloPay"}, status=response.status_code)

            return Response(response_data)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
