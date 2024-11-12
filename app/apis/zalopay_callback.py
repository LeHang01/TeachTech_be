import json
import string
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from app.models import Payment, User  # Thêm import cho User nếu chưa có

class ZaloPayCallback(APIView):

    def post(self, request):
        result = {}

        # Lấy paymentId từ callback request
        callback_data_str = request.data.get('data')
        callback_data = json.loads(callback_data_str)
        app_user = callback_data.get("app_user", None)
        payment_id = int(app_user)

        if not payment_id:
            result['return_code'] = 0
            result['return_message'] = 'Missing paymentId'
            return JsonResponse(result)

        try:
            # Truy vấn thông tin thanh toán từ paymentId
            payment = Payment.objects.get(id=payment_id)
            full_name = payment.full_name
            birth_date = payment.birth_date

            # Tạo username và password cho người dùng
            username = self.generate_username(full_name, birth_date)
            password = self.generate_password(full_name, birth_date)
            print(password)

            # Kiểm tra xem người dùng đã tồn tại chưa, nếu chưa thì tạo mới
            user = User.objects.filter(username=username).first()
            if not user:
                # Tạo người dùng mới nếu chưa tồn tại
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=full_name.split()[0],  # Họ
                    last_name=" ".join(full_name.split()[1:]),  # Tên
                    email="user@example.com",  # Email (có thể bạn cần cung cấp email hợp lệ)
                    is_active=True,  # Đảm bảo người dùng mới có thể đăng nhập
                    is_staff=False,  # Không phải nhân viên (tùy theo yêu cầu)
                    is_superuser=False,  # Không phải superuser (tùy theo yêu cầu)
                    payment=payment
                )
                user_dict = user.__dict__
                user_dict.pop('_state', None)
            else:
                user.set_password(password)
                user.payment = payment
                user.save()
                user_dict = user.__dict__
                user_dict.pop('_state', None)

            result['return_code'] = 1
            result['return_message'] = 'Success'
            result['username'] = username
            result['password'] = password
            result['redirect_url'] = 'http://localhost:3000/registration-success'

        except Payment.DoesNotExist:
            result['return_code'] = 0
            result['return_message'] = 'Payment not found'
        except Exception as e:
            result['return_code'] = 0
            result['return_message'] = f"Error: {str(e)}"

        return JsonResponse(result)

    def generate_username(self, full_name, birth_date):
        """Generate username based on full name and birth date"""
        first_name = full_name.split()[0].lower()  # Lấy tên đầu tiên trong full name và chuyển thành chữ thường

        # Chuyển birth_date thành chuỗi để lấy năm và tháng
        birth_date_str = birth_date.strftime('%Y-%m-%d')  # Đổi đối tượng datetime.date thành chuỗi "YYYY-MM-DD"

        birth_year = birth_date_str.split('-')[0]  # Lấy năm sinh từ chuỗi
        birth_month = birth_date_str.split('-')[1]  # Lấy tháng sinh từ chuỗi

        # Tạo username theo định dạng: "ký tự đầu của tên" + "tháng" + "2 chữ số cuối của năm"
        username = f"{first_name[0]}{birth_month}{birth_year[-2:]}"

        return username

    def generate_password(self, full_name, birth_date):
        """Generate a password by combining full name and birth date"""
        # Chúng ta có thể kết hợp `full_name` và `birth_date` để tạo mật khẩu
        birth_date_str = birth_date.strftime('%Y%m%d')  # Đổi đối tượng datetime.date thành chuỗi "YYYYMMDD"
        password = f"{full_name.replace(' ', '')}{birth_date_str}"  # Kết hợp full_name (bỏ dấu cách) và birth_date
        return password  # Trả về mật khẩu đã tạo