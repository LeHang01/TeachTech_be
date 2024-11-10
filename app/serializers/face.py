import base64
import json

import numpy as np
from io import BytesIO
from PIL import Image
from keras_facenet import FaceNet
from mtcnn import MTCNN
from rest_framework import serializers

from app.models import User


class FaceSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.CharField()  # Nhận các chuỗi base64
    )
    user_id = serializers.IntegerField(required=False)  # ID người dùng để cập nhật embedding

    @staticmethod
    def record(data):
        images = data['images']
        user_id = data['user_id']

        if not images:
            raise serializers.ValidationError("Danh sách hình ảnh không thể rỗng.")

        # Khởi tạo MTCNN và Keras-Facenet
        mtcnn = MTCNN()
        model = FaceNet()

        embeddings = []
        for img_base64 in images:
            # Giải mã base64 thành hình ảnh
            format, imgstr = img_base64.split(';base64,')  # Tách định dạng và dữ liệu base64
            img_data = base64.b64decode(imgstr)  # Giải mã dữ liệu base64
            image = Image.open(BytesIO(img_data)).convert("RGB")  # Chuyển đổi byte thành hình ảnh

            image = np.array(image)

            # Phát hiện khuôn mặt
            boxes = mtcnn.detect_faces(image)
            if boxes:
                # Lấy embedding cho từng khuôn mặt
                for face in boxes:
                    x1, y1, width, height = face['box']
                    x2, y2 = x1 + width, y1 + height
                    face_image = image[y1:y2, x1:x2]

                    # Resize và chuẩn hóa hình ảnh
                    face_image = Image.fromarray(face_image)
                    face_image = face_image.resize((160, 160))  # Kích thước chuẩn cho FaceNet
                    face_array = np.asarray(face_image) / 255.0  # Chuẩn hóa pixel về [0, 1]
                    face_array = np.expand_dims(face_array, axis=0)  # Thêm batch dimension

                    # Tính toán embedding
                    embedding = model.embeddings(face_array)
                    embeddings.append(embedding[0].tolist())  # Chỉ lấy embedding đầu tiên

        # Cập nhật embedding cho người dùng
        user = User.objects.get(id=user_id)
        user.embedding = embeddings
        user.save()

        return embeddings

    @staticmethod
    def recognize(data):
        image_base64_list = data['images']  # Lấy danh sách hình ảnh

        # Khởi tạo MTCNN và Keras-Facenet
        mtcnn = MTCNN()
        model = FaceNet()

        for image_base64 in image_base64_list:
            # Giải mã base64 thành hình ảnh
            format, imgstr = image_base64.split(';base64,')  # Tách định dạng và dữ liệu base64
            img_data = base64.b64decode(imgstr)  # Giải mã dữ liệu base64
            image = Image.open(BytesIO(img_data)).convert("RGB")  # Chuyển đổi byte thành hình ảnh
            image = np.array(image)

            # Phát hiện khuôn mặt
            boxes = mtcnn.detect_faces(image)
            if not boxes:
                continue  # Nếu không phát hiện được khuôn mặt, tiếp tục với hình ảnh tiếp theo

            # Tính toán embedding cho từng khuôn mặt phát hiện
            for face in boxes:
                x1, y1, width, height = face['box']
                x2, y2 = x1 + width, y1 + height
                face_image = image[y1:y2, x1:x2]

                # Resize và chuẩn hóa hình ảnh
                face_image = Image.fromarray(face_image)
                face_image = face_image.resize((160, 160))  # Kích thước chuẩn cho FaceNet
                face_array = np.asarray(face_image) / 255.0  # Chuẩn hóa pixel về [0, 1]
                face_array = np.expand_dims(face_array, axis=0)  # Thêm batch dimension

                # Tính toán embedding
                embedding = model.embeddings(face_array)[0].tolist()  # Chỉ lấy embedding đầu tiên

                # Tìm người dùng tương ứng bằng cách so sánh embedding
                threshold = 0.5  # Ngưỡng để so sánh
                users = User.objects.all()  # Lấy tất cả người dùng trong database

                for user in users:
                    if user.embedding:  # Kiểm tra xem embedding có tồn tại không
                        # Tính toán khoảng cách Euclidean giữa hai embedding
                        distance = np.linalg.norm(np.array(user.embedding) - np.array(embedding))
                        print(distance)
                        if distance < threshold:  # Nếu khoảng cách nhỏ hơn ngưỡng
                            return user  # Trả về người dùng đầu tiên tìm thấy

        raise serializers.ValidationError("Không tìm thấy người dùng nào khớp với khuôn mặt.")