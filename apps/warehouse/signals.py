from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.warehouse.models import Bin


# @receiver(signal=post_save, sender=Bin)
# def generate_barcode(sender, instance, created, **kwargs):
#     pass