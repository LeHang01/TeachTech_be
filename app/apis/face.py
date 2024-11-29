from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.serializers.face import FaceSerializer, FaceRecognizeSerializer, FaceRecordSerializer


class FaceViewSet(viewsets.GenericViewSet):
    serializer_class = FaceSerializer

    @swagger_auto_schema(method='post', request_body=FaceRecordSerializer)
    @action(detail=False, methods=['post'], url_path='record')
    def record(self, request):
        serializer = FaceRecordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.record(images=request.data['images'], user_id=request.data['user_id'])
        return Response('Ghi nhận khuôn mặt thành công', status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=FaceRecognizeSerializer)
    @action(detail=False, methods=['post'], url_path='recognize')
    def recognize(self, request):
        serializer = FaceRecognizeSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.recognize(images=request.data['images'])
        print(data)
        return Response(data, status=status.HTTP_200_OK)