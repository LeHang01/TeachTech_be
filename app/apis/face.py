from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.serializers.face import FaceSerializer


class FaceViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = FaceSerializer

    @swagger_auto_schema(method='post', request_body=FaceSerializer)
    @action(detail=False, methods=['post'], url_path='record')
    def record(self, request):
        serializer = FaceSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.record(request.data)
        return Response('Ghi nhận khuôn mặt thành công', status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=FaceSerializer)
    @action(detail=False, methods=['post'], url_path='recognize')
    def recognize(self, request):
        serializer = FaceSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.recognize(request.data)
        print(data)
        return Response(str(data.email), status=status.HTTP_200_OK)