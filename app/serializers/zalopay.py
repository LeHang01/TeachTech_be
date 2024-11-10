# serializers/zalopay_serializers.py

from rest_framework import serializers


class ZaloPayOrderSerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    app_trans_id = serializers.CharField(max_length=50)
    app_user = serializers.CharField(max_length=50)
    app_time = serializers.IntegerField()
    embed_data = serializers.JSONField()
    item = serializers.JSONField()
    amount = serializers.IntegerField()
    description = serializers.CharField(max_length=200)
    bank_code = serializers.CharField(max_length=50)
    mac = serializers.CharField(max_length=64)


class ZaloPayCallbackSerializer(serializers.Serializer):
    data = serializers.CharField()
    mac = serializers.CharField()
    type = serializers.IntegerField()
