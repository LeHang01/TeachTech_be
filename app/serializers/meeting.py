# payments/serializers.py
from rest_framework import serializers

from app.models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
