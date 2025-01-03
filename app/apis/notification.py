from bson import ObjectId
from django.conf import settings  # Để lấy thông tin cấu hình từ settings
from drf_yasg.utils import swagger_auto_schema
from pymongo import MongoClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationViewSet(APIView):
    @swagger_auto_schema(
        responses={
            200: "Success",
            404: "No notifications found",
            500: "Server Error"
        }  # Mô tả mã trả về
    )
    def get(self, request, notification_id):
        """
        API để lấy danh sách thông báo theo ID từ MongoDB
        """
        try:
            # Kết nối tới MongoDB
            with MongoClient(settings.MONGODB_URI) as client:
                db = client[settings.MONGO_DB_NAME]
                notifications_collection = db["notifications"]

                # Tìm tất cả thông báo cho user với notification_id
                notifications = notifications_collection.find({"to-notify-user": str(notification_id)}).sort("created_at", -1)

                # Chuyển đổi kết quả thành danh sách
                notification_list = []
                for notification in notifications:
                    if notification_id in notification.get("seen_users", []):
                        notification["is_seen"] = True
                    else:
                        notification["is_seen"] = False
                    notification_list.append({
                        'id': str(notification['_id']),  # Chuyển ObjectId thành string
                        'full_name': notification.get('full_name', ''),
                        'phone_number': notification.get('phone_number', ''),
                        'address': notification.get('address', ''),
                        'course_name': notification.get('course_name', ''),
                        'course_price': notification.get('course_price', 0),
                        'teacher_name': notification.get('teacher_name', ''),
                        'time': notification.get('time', ''),
                        'to-notify-user': notification.get('to-notify-user', ''),
                        'is_seen': notification.get('is_seen', ''),
                        'seen_users': notification.get('seen_users', []),
                        'created_at': notification.get('created_at')
                        if notification.get('created_at') else None,
                    })

                if not notification_list:
                    # Nếu không tìm thấy thông báo, trả về lỗi 404
                    return Response({"message": "No notifications found"}, status=status.HTTP_404_NOT_FOUND)

                return Response(notification_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Xử lý lỗi
            return Response({"message": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: "Notification marked as read",
            400: "Invalid request",
            500: "Server Error"
        }
    )
    def put(self, request, user_id, notification_id):
        """
        API để đánh dấu thông báo là đã đọc
        """
        try:
            # Chuyển đổi notification_id sang ObjectId
            notification_object_id = ObjectId(notification_id)

            with MongoClient(settings.MONGODB_URI) as client:
                db = client[settings.MONGO_DB_NAME]
                collection = db["notifications"]

                # Tìm và cập nhật thông báo cụ thể với notification_id và user_id
                notification = collection.find_one(
                    {"_id": notification_object_id, "to-notify-user": user_id}
                )

                if not notification:
                    return Response({"message": "Notification not found or user not authorized"},
                                    status=status.HTTP_404_NOT_FOUND)

                # Kiểm tra nếu user_id chưa có trong danh sách seen_users thì thêm vào
                if user_id not in notification.get("seen_users", []):
                    collection.update_one(
                        {"_id": notification_object_id},
                        {"$addToSet": {"seen_users": user_id}}  # Thêm vào danh sách mà không trùng lặp
                    )
                    return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Notification already marked as read"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
