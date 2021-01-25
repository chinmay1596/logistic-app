from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Create default super Admin'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name="Super Admin")
        with transaction.atomic():
            user = UserModel.objects.create_user('admin@test.com', 'admin123')
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.is_verified = True
            user.save()
        self.stdout.write('Successfully created Super Admin...')
