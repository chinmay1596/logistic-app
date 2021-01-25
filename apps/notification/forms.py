from apps.notification.models import Notification
from apps.commons.mixins.commons import DynamicFieldsModelForm
from fcm_django.models import FCMDevice


class CreateFCMDeviceForm(DynamicFieldsModelForm):
    class Meta:
        model = FCMDevice
        fields = ['user', 'registration_id', 'type']


class ReadNotificationUpdateForm(DynamicFieldsModelForm):
    class Meta:
        model = Notification
        fields = ['read']
