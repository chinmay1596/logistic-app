from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
# custom user manager
from sorl.thumbnail import ImageField

from apps.account.constants import USER_TYPES, GENDER_CHOICES
from apps.commons.utils.commons import get_upload_path


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Address(models.Model):
    country_code = models.CharField(max_length=45)
    country_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    locality_name = models.CharField(max_length=200)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], help_text='Enter Values between -90 to 90',
        null=True, blank=True)
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], help_text='Enter Values between -180 to 180',
        null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ('country_code', 'country_name', 'state', 'city_name', 'street', 'locality_name')

    def __str__(self):
        return self.country_name

    @property
    def address(self):
        return f'{self.street}, {self.city_name}, {self.state}, {self.country_name}'


class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    address = models.CharField(max_length=64, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    driving_licence = models.CharField(max_length=60, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    image = ImageField(null=True, blank=True, upload_to=get_upload_path)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email

    def get_address(self):
        return self.address if self.address else 'N|A'
