# services/fcm_sender.py
from pyfcm import FCMNotification

FCM_SERVER_KEY = "YOUR_FCM_KEY"  # 之後貼你自己的

push_service = FCMNotification(api_key=FCM_SERVER_KEY)

def send_push(topic, title, body):
    push_service.notify_topic_subscribers(
        topic_name=topic,
        message_title=title,
        message_body=body
    )
