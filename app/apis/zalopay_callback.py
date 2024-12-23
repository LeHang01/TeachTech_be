import json
import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from pymongo import MongoClient
from rest_framework.views import APIView
from unidecode import unidecode

from app.models import Payment, User  # Thêm import cho User nếu chưa có
from app.task import send_notification_batch


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
            birth_date = payment.birth_date
            full_name = payment.full_name
            phone_number = payment.phone_number
            address = payment.address
            course_name = payment.course.course_name
            course_price = payment.course.price
            teacher_name = payment.course.teacher.name
            teacher_id = payment.course.teacher.id
            user = User.objects.get(teacher__id=teacher_id)
            user_id = user.id
            seen_users = []
            channels = [
                f'{str(user_id)}',
            ]
            response_data = {
                'full_name': full_name,
                'phone_number': phone_number,
                'address': address,
                'course_name': course_name,
                'course_price': float(course_price),
                'teacher_name': teacher_name,
                'to-notify-user': str(user_id),
                'seen_users': seen_users,
                'created_at': datetime.utcnow(),
            }
            # Log dữ liệu trước khi lưu
            with MongoClient(settings.MONGODB_URI) as client:
                db = client[settings.MONGO_DB_NAME]
                notifications = db["notifications"]
                notifications.insert_one(response_data)

            # Log dữ liệu sau khi lưu
            response_data['_id']= str(response_data.get('_id'))
            response_data = {**response_data, 'type': "Payment"}

            # Kiểm tra việc gửi thông báo
            send_notification_batch.delay(channels=channels, notification_data=response_data)

            # Kiểm tra dữ liệu cuối cùng
            print(f"Notification data sent: {response_data}")

            # Tạo username và password cho người dùng
            username = self.generate_username(full_name, birth_date)
            password = self.generate_password(full_name, birth_date)
            print(password)

            # Kiểm tra xem người dùng đã tồn tại chưa, nếu chưa thì tạo mới
            user = User.objects.filter(username=username).first()
            if not user:
                # Tạo người dùng mới nếu chưa tồn tại
                user = User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=full_name.split()[0],  # Họ
                    last_name=" ".join(full_name.split()[1:]),  # Tên
                    email=f"{username}@gmail.com",  # Email (có thể bạn cần cung cấp email hợp lệ)
                    is_active=True,  # Đảm bảo người dùng mới có thể đăng nhập
                    is_staff=False,  # Không phải nhân viên (tùy theo yêu cầu)
                    is_superuser=False,  # Không phải superuser (tùy theo yêu cầu)
                    payment=payment
                )
                print('user', user)
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

    def acronym_format(self, acronym_str):
        return unidecode(''.join(word[0] for word in acronym_str.split()).lower())

    def unsigned_format(self, unsigned_str):
        return unidecode(unsigned_str.lower())

    def generate_username(self, full_name, birth_date):
        matches = re.match(r"((\S+\s)*\S+)\s+(\S+)", full_name)
        last_middle_name = matches.group(1)
        first_name = matches.group(3)

        last_middle_name_acronym = self.acronym_format(last_middle_name)
        first_name_unsigned = self.unsigned_format(first_name)
        date_of_birth_short = birth_date.strftime("%d%m%y")

        regex = "".join([last_middle_name_acronym, first_name_unsigned, date_of_birth_short])
        return regex

    def generate_password(self, full_name, birth_date):
        full_name_unsigned = unidecode(full_name.strip().lower())

        # Tách từng từ trong tên và lấy ký tự đầu tiên của mỗi từ
        initials = "".join(word[0] for word in full_name_unsigned.split() if word)

        # Lấy ngày tháng năm từ birth_date
        date_str = birth_date.strftime('%d%m%y')  # 2 số ngày, 2 số tháng, 2 số cuối năm

        # Tạo mật khẩu
        password = f"{initials}_{date_str}"
        return password
