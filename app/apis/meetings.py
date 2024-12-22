import logging
from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Document, Meeting, User, Course, Payment, Attendance
from app.serializers.meeting import MeetingSerializer

# Khởi tạo logger
logger = logging.getLogger(__name__)


class MeetingViewSet(viewsets.GenericViewSet, generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get(self, request):
        # Lấy tất cả các cuộc họp và tài liệu
        meetings = Meeting.objects.all()
        documents = Document.objects.all()

        # Tạo một dictionary ánh xạ tài liệu theo ID
        document_map = {doc.id: doc.file_url for doc in documents}

        # Chuẩn bị dữ liệu trả về
        meeting_data = []
        for meeting in meetings:
            # Lấy danh sách ID từ attachments (giả sử là danh sách ID)
            attachment_ids = meeting.attachments

            # Tìm các tài liệu tương ứng
            meeting_documents = [
                {"id": doc_id, "file_url": document_map[doc_id]}
                for doc_id in attachment_ids
                if doc_id in document_map
            ]

            # Thêm dữ liệu cuộc họp và tài liệu
            meeting_data.append({
                "id": meeting.id,
                "topic": meeting.topic,
                "date_time": meeting.date_time,
                "status": meeting.status,
                "attachments": meeting_documents,
                "platform": meeting.platform,
                "link": meeting.link,
                "content": meeting.content,
            })

        return Response(meeting_data)

    @action(detail=True, methods=['get'])
    def get_by_id(self, request, pk=None):
        try:
            # Lấy tất cả các cuộc họp có participant tương ứng với `pk`
            meetings = Meeting.objects.filter(participants__contains=[pk])

            # Lấy tất cả các tài liệu
            documents = Document.objects.all()

            # Tạo một dictionary ánh xạ tài liệu theo ID
            document_map = {doc.id: doc.file_url for doc in documents}

            # Chuẩn bị dữ liệu trả về
            meeting_data = []
            for meeting in meetings:
                # Lấy danh sách ID từ attachments (giả sử là danh sách ID lưu trong dạng JSON)
                attachment_ids = meeting.attachments if isinstance(meeting.attachments, list) else []

                # Tìm các tài liệu tương ứng
                meeting_documents = [
                    {"id": doc_id, "file_url": document_map.get(doc_id)}
                    for doc_id in attachment_ids
                    if doc_id in document_map
                ]

                # Thêm dữ liệu cuộc họp và tài liệu vào danh sách trả về
                meeting_data.append({
                    "id": meeting.id,
                    "topic": meeting.topic,
                    "date_time": meeting.date_time,
                    "status": meeting.status,
                    "attachments": meeting_documents,
                    "platform": meeting.platform,
                    "link": meeting.link,
                    "content": meeting.content,
                    "has_attended": meeting.has_attended,
                })

            # Trả về kết quả
            return Response(meeting_data, status=200)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found."}, status=404)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def create(self, request, *args, **kwargs):
        document_ids = []

        # Tạo client S3 với MinIO
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Kiểm tra xem có tệp đính kèm không
        if 'files[]' in request.FILES:
            files = request.FILES.getlist('files[]')  # Lấy danh sách tệp đính kèm
            for file in files:
                filename = file.name
                try:
                    # Tải tệp lên MinIO
                    today_date = datetime.today().strftime('%d-%m-%Y')
                    s3_client.put_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Key=f"documents/{today_date}/{filename}",
                        Body=file,
                        ContentType=file.content_type
                    )
                    # Tạo đối tượng Document và lưu vào cơ sở dữ liệu
                    document = Document.objects.create(file_url=f"documents/{today_date}/{filename}")
                    document_ids.append(document.id)  # Lưu ID của tài liệu vào danh sách

                except (NoCredentialsError, PartialCredentialsError) as e:
                    logger.error('MinIO credentials error: %s', str(e))
                    return Response({'error': 'MinIO credentials error'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error('Error saving file %s to MinIO: %s', file.name, str(e))
                    return Response({'error': 'File upload failed'}, status=status.HTTP_400_BAD_REQUEST)

            # Bước 1: Lấy teacher_id từ user_id
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # Kiểm tra xem người dùng có phải là giáo viên không
        if not user.is_teacher:
            return Response({'error': 'User is not a teacher'}, status=status.HTTP_400_BAD_REQUEST)

        # Bước 2: Lấy course_id từ teacher_id
        teacher = user.teacher  # Lấy teacher liên kết với user
        if not teacher:
            return Response({'error': 'Teacher not found for user'}, status=status.HTTP_400_BAD_REQUEST)

        courses = Course.objects.filter(teacher=teacher)  # Lấy tất cả khóa học của giáo viên
        print(courses)
        if not courses.exists():
            return Response({'error': 'No courses found for the teacher'}, status=status.HTTP_400_BAD_REQUEST)

        # Bước 3: Lấy payment_id từ các course_id
        course_ids = courses.values_list('id', flat=True)
        payments = Payment.objects.filter(course__in=course_ids)  # Lấy tất cả thanh toán liên kết với khóa học
        payment_ids = payments.values_list('id', flat=True)

        if not payment_ids:
            return Response({'error': 'No payments found for these courses'}, status=status.HTTP_400_BAD_REQUEST)

        # Bước 4: Lấy tất cả các User có payment_id giống nhau
        users_with_same_payment = User.objects.filter(payment__id__in=payment_ids)

        # Trả về danh sách các User
        user_ids = list(users_with_same_payment.values_list('id', flat=True))
        print(user_ids)
        meeting = Meeting(
            topic=request.data.get('topic'),
            platform=request.data.get('platform'),
            link=request.data.get('link'),
            date_time=request.data.get('dateTime'),
            content=request.data.get('content'),
            status="Chưa bắt đầu",  # Mặc định là "Chưa bắt đầu"
            attachments=document_ids,
            participants=user_ids
        )

        # Lưu Meeting vào database
        meeting.save()
        for user_id in user_ids:
            user_instance = User.objects.get(id=user_id)
            Attendance.objects.create(
                user=user_instance,
                meeting=meeting,
                status="Chưa tham gia",  # Trạng thái mặc định là "Chưa tham gia"
            )
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Fetch a specific meeting by ID
        meeting = get_object_or_404(Meeting, pk=pk)
        meeting_data = {
            "id": meeting.id,
            "topic": meeting.topic,
            "date_time": meeting.date_time,
            "status": meeting.status,
            "platform": meeting.platform,
            "link": meeting.link,
            "content": meeting.content,
        }
        return Response(meeting_data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Cập nhật trạng thái của một cuộc họp.
        """
        meeting = get_object_or_404(Meeting, pk=pk)

        # Lấy trạng thái mới từ request
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'Trạng thái không được cung cấp'}, status=status.HTTP_400_BAD_REQUEST)

        # Cập nhật trạng thái cuộc họp
        meeting.status = new_status
        meeting.save()

        return Response({
            'message': 'Cập nhật trạng thái thành công',
            'meeting_id': meeting.id,
            'new_status': meeting.status
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_meeting(self, request, pk=None):
        # Lấy đối tượng Meeting theo ID
        meeting = get_object_or_404(Meeting, pk=pk)

        # Lấy giá trị has_attended từ request
        attendance_status = request.data.get("has_attended")

        if attendance_status:
            # Cập nhật trạng thái điểm danh cho cuộc họp
            meeting.has_attended = attendance_status
            meeting.save()
            if meeting.has_attended == "Đã điểm danh":
                # Lọc các Attendance có trạng thái "Chưa tham gia"
                attendances_to_update = Attendance.objects.filter(meeting=meeting, status="Chưa tham gia")

                # Cập nhật trạng thái thành "Vắng" và lý do vắng là "Không chính đáng"
                attendances_to_update.update(
                    status="Vắng",
                    absence_reason_type="Không chính đáng"
                )
            return Response({"detail": "Meeting updated successfully."}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)