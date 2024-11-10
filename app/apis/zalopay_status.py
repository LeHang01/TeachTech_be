# apis/zalopay_status.py
import time

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
import hmac, hashlib, json, requests


class ZaloPayOrderStatus(APIView):
    def get(self, request, app_trans_id):
        app_id = settings.ZALOPAY_CONFIG["APP_ID"]
        key1 = settings.ZALOPAY_CONFIG["KEY1"]
        endpoint = settings.ZALOPAY_CONFIG["STATUS_ENDPOINT"]

        mac_data = f"{app_id}|{app_trans_id}|{int(time.time() * 1000)}"
        mac = hmac.new(key1.encode(), mac_data.encode(), hashlib.sha256).hexdigest()

        params = {
            "app_id": app_id,
            "app_trans_id": app_trans_id,
            "mac": mac,
        }

        response = requests.get(endpoint, params=params)
        return Response(response.json())
