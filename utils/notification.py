from apps.notification.models import Notification
from fcm_django.models import FCMDevice


def send_notification(user_id, title, message, data, click_action):
    try:
        Notification.objects.create(user_id=user_id, title=title, message=message, data=data, click_action=click_action)
        device = FCMDevice.objects.filter(user=user_id).last()
        result = device.send_message(title=title, body=message, data=data, sound=True, click_action=click_action)
        return result
    except:
        pass
