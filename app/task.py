from datetime import datetime
from typing import List, Union

from celery import shared_task
from pusher import Pusher
from django.conf import settings

from app.utils import convert_datetime_to_string

pusher_client = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)


@shared_task
def sent_notification(channel, notification_data):
    pusher_client.trigger(f'{channel}', 'my-event', {
        'title': channel,
        'message': notification_data
    })


@shared_task
def send_notification_batch(channels: List[Union[str]], notification_data: dict):
    batch = []
    for channel in channels:
        batch.append({
            'channel': channel,
            'name': notification_data.get("type", "Unknown"),  # Default to "Unknown" if type is missing
            'data': {
                'full_name': notification_data.get('full_name', None),
                '_id': notification_data.get('_id', None),
                'phone_number': notification_data.get('phone_number', None),
                'address': notification_data.get('address', None),
                'course_name': notification_data.get('course_name', None),
                'course_price': notification_data.get('course_price', None),
                'teacher_name': notification_data.get('teacher_name', None),
                'to-notify-user': notification_data.get('to-notify-user', None),
                'seen_users': notification_data.get('seen_users', []),  # Default to empty list
                'created_at': notification_data.get('created_at', datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S'),
                'time': notification_data.get('time', None),

            }
        })

    pusher_client.trigger_batch(batch, False)
