import base64

import cv2
import numpy as np
from keras_facenet import FaceNet
from mtcnn import MTCNN
from rest_framework import serializers

from app.models import User

mtcnn = MTCNN()
model = FaceNet()


class FaceSerializer(serializers.Serializer):
    def record(self, images, user_id):
        try:
            frames = [self.load_image_from_base64(image) for image in images]
            for frame in frames:
                faces = mtcnn.detect_faces(frame)
                self.handle_faces(faces, user_id, frame)
        except Exception as e:
            raise serializers.ValidationError(e)

    def handle_faces(self, faces, user_id: int, frame):
        """Handle detected faces and update the database."""
        person_embeddings = {}

        for face in faces:
            embedding = self.extract_embedding(face, frame)
            if embedding is not None:
                if user_id in person_embeddings:
                    person_embeddings[user_id].append(embedding)
                else:
                    person_embeddings[user_id] = [embedding]

        for user_id, embeddings_list in person_embeddings.items():
            mean_embedding = np.mean(embeddings_list, axis=0).tolist()
            if not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError("Tài khoản không tồn tại!")

            user = User.objects.get(id=user_id)
            user.embedding = mean_embedding
            user.save()
            print('mean_embedding', mean_embedding)
            print('user', user)
        return "Thành công! Bạn đã ghi nhận khuôn mặt."

    def load_image_from_base64(self, image_base64: str):
        """Decode a base64 image and return it as a cv2 frame."""
        try:
            img_data = base64.b64decode(image_base64.split(',')[1])
            np_array = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            if frame is None or frame.size == 0:
                return None
            return frame
        except Exception as e:
            return None

    def extract_embedding(self, face, frame):
        """Extract the embedding from the detected face."""
        try:
            x, y, width, height = face['box']

            # Ensure the coordinates are within the image boundaries
            if x < 0 or y < 0 or x + width > frame.shape[1] or y + height > frame.shape[0]:
                return None

            # Extract the face region from the image
            face_region = frame[y:y + height, x:x + width]

            # Validate if the face_region is a valid numpy array
            if face_region is None or face_region.size == 0:
                return None

            rgb_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
            resized_face = cv2.resize(rgb_face, (160, 160))  # Resize to (160, 160)
            input_face = np.expand_dims(resized_face, axis=0)  # Shape (1, 160, 160, 3)

            embeddings = model.embeddings(input_face)
            if embeddings is not None and embeddings.shape[0] > 0:
                return embeddings[0]
            else:
                return None
        except Exception as e:
            return None

    def recognize(self, images):
        try:
            frames = [self.load_image_from_base64(image) for image in images]
            for frame in frames:
                faces = mtcnn.detect_faces(frame)
                if faces:
                    for face in faces:
                        embedding = self.extract_embedding(face, frame)
                        if embedding is not None:
                            recognized_label = self.match_embedding(embedding)
                            if recognized_label:  # Nếu nhận diện thành công
                                user = User.objects.filter(id=recognized_label).first()
                                if user and user.payment:
                                    # Lấy thông tin từ bảng Payment
                                    return {
                                        "user_id": user.id,
                                        "full_name": user.payment.full_name,
                                        "birth_date": user.payment.birth_date,
                                        "gender": user.payment.gender,
                                        "phone_number": user.payment.phone_number,
                                        "address": user.payment.address,
                                        "course": user.payment.course.course_name,
                                        "payment_date": user.payment.payment_date,
                                        "status": "recognized"
                                    }
                                raise serializers.ValidationError(
                                    "Người dùng nhận diện nhưng không tìm thấy thông tin thanh toán.")
                            else:
                                raise serializers.ValidationError("Khuôn mặt không được nhận dạng!")
        except Exception as e:
            raise serializers.ValidationError(e)

    def match_embedding(self, embedding: np.ndarray):
        """Compare the given embedding with stored embeddings and return the matching label."""
        try:
            users = User.objects.all()
            for user in users:
                if user.embedding:
                    stored_embedding = np.array(user.embedding)
                    similarity = np.dot(embedding, stored_embedding) / (
                            np.linalg.norm(embedding) * np.linalg.norm(stored_embedding))
                    print('++++++++++++', similarity)
                    if similarity >= 0.5:
                        return user.id
            return None
        except Exception as e:
            print(e)
            return None


class FaceRecordSerializer(FaceSerializer):
    images = serializers.ListField(
        child=serializers.CharField()  # Nhận các chuỗi base64
    )
    user_id = serializers.IntegerField(required=True)  # ID người dùng để cập nhật embedding


class FaceRecognizeSerializer(FaceSerializer):
    user_id = serializers.IntegerField(required=True)
    meetingId = serializers.IntegerField(required=True)
    images = serializers.ListField(
        child=serializers.CharField()  # Nhận các chuỗi base64
    )
