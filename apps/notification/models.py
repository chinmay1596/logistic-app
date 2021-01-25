from django.db import models
from django.contrib.auth import get_user_model
from apps.commons.models.commons import BaseModel, SerializedModal

User = get_user_model()


class Notification(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_user')
    title = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)
    click_action = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.user} title:{self.title} msg:{self.message} data:{self.data}) read:{self.read}"

class SerializeNotification(SerializedModal, Notification):
    model_reference = {
        'id': 'id',
        'user': {
            'id': 'id',
        },
        'title': 'title',
        'message': 'message',
        'data': 'data',
        'read': 'read',
        'created_at': 'created_at',
        'click_action': 'click_action',
    }

    class Meta:
        proxy = True
        ordering = ['id']