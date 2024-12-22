from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Attendance, Meeting


class AttendanceViewSet(viewsets.ViewSet):

    def list(self, request, meeting_id=None):
        # Fetch the meeting object by its ID
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Fetch all attendance records for the specified meeting
        attendance_data = []
        attendances = Attendance.objects.filter(meeting=meeting)  # use filter() instead of get()

        # Ensure that attendances is iterable
        if attendances.exists():  # check if there are attendance records
            for attendance in attendances:
                dob = attendance.user.payment.birth_date
                student_name = attendance.user.payment.full_name
                user_id = attendance.user.id
                attendance_id = attendance.id
                attendance_data.append(
                    {
                        'attendance_id': attendance_id,
                        'user_id': user_id,
                        'dob': dob,
                        "student_name": student_name,
                        "status": attendance.status,
                        "attendance_time": attendance.check_in,
                        "absence_reason_type": attendance.absence_reason_type,
                        "has_attended": meeting.has_attended,
                    }
                )
        else:
            return Response({"detail": "No attendance records found for this meeting."}, status=404)

        # Return the serialized data as a JSON response
        return Response(attendance_data)

    @action(detail=True, methods=["patch"])
    def update_reason(self, request, pk=None):
        """
        Cập nhật lý do vắng của một học viên cụ thể.
        """
        attendance = get_object_or_404(Attendance, id=pk)

        absence_reason_type = request.data.get("absence_reason_type", None)
        if not absence_reason_type:
            return Response({"detail": "absence_reason_type is required."}, status=400)

        attendance.absence_reason_type = absence_reason_type
        attendance.save()

        return Response({"detail": "Attendance reason updated successfully."}, status=200)