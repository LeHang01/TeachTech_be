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
            'name': notification_data["type"],
            'data': {
                'full_name': notification_data['full_name'],
                '_id': notification_data['_id'],
                'phone_number': notification_data['phone_number'],
                'address': notification_data['address'],
                'course_name': notification_data['course_name'],
                'course_price': notification_data['course_price'],
                'teacher_name': notification_data['teacher_name'],
                'to-notify-user': notification_data['to-notify-user'],
                'seen_users': notification_data['seen_users'],
                'created_at': notification_data['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            }
        })

    pusher_client.trigger_batch(batch, False)
