import hashlib
import hmac
import json
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.parse import parse_qs


class ZaloPayCallback(APIView):

    def post(self, request):
        result = {}
        try:
            # In ra dữ liệu nhận được từ ZaloPay callback
            print(f"Received callback data: {request.data}")

            # Lấy dữ liệu từ callback
            data_str = request.data.get('data', '')
            req_mac = request.data.get('mac', '')

            if not data_str or not req_mac:
                result['return_code'] = 0
                result['return_message'] = 'Missing data or mac'
                return Response(result)

            # Tính toán MAC với KEY2 từ ZaloPay config
            mac = hmac.new(settings.ZALOPAY_CONFIG['KEY2'].encode(), data_str.encode(), hashlib.sha256).hexdigest()

            # Kiểm tra tính hợp lệ của MAC
            if req_mac != mac:
                result['return_code'] = -1
                result['return_message'] = 'mac not equal'
            else:
                # Thanh toán thành công
                data_json = json.loads(data_str)
                print(f"Update order's status = success where app_trans_id = {data_json['app_trans_id']}")

                # In chi tiết dữ liệu nhận được
                print("Callback data:", data_json)

                # Thực hiện cập nhật trạng thái giao dịch trong hệ thống của bạn
                result['return_code'] = 1
                result['return_message'] = 'success'
        except Exception as e:
            print(f"Error: {e}")
            result['return_code'] = 0
            result['return_message'] = str(e)

        return Response(result)


