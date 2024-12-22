from rest_framework import serializers
from app.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'meeting', 'status', 'check_in', 'absence_reason_type', 'notes', 'created_at', 'updated_at']
