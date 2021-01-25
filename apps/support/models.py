from django.db import models
from apps.commons.models.commons import BaseModel
from apps.customer.models import Customer
from .constants import GENERATED_BY
from django.contrib.auth import get_user_model

User = get_user_model()


class Documents(BaseModel):
    files = models.FileField(upload_to='files/support', null=True, blank=True)

    def __str__(self):
        return str(self.files)

    @property
    def filesize(self):
        x = self.files.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' Mb'
        else:
            value = round(x / 1000000000, 2)
            ext = ' Gb'
        return str(value) + ext


class Ticket(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    type_of_issue = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    generated_by = models.CharField(
        max_length=20, choices=GENERATED_BY, null=True, blank=True)
    documents = models.ManyToManyField(Documents, blank=True)

    def __str__(self):
        return self.title


class Chat(BaseModel):
    sender = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True, blank=True)
    file_upload = models.FileField(
        upload_to='files/support', null=True, blank=True)

    def __str__(self):
        return str(self.ticket)

    @property
    def filesize(self):
        x = self.file_upload.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' Mb'
        else:
            value = round(x / 1000000000, 2)
            ext = ' Gb'
        return str(value) + ext
