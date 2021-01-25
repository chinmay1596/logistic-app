from django import forms
from apps.commons.mixins.commons import DynamicFieldsModelForm
from .models import Chat


class SupportChatForm(DynamicFieldsModelForm):
    message = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Chat
        fields = ['message', 'file_upload']

        placeholder = {
            'message': 'Write your message here',
        }
