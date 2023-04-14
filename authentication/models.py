import datetime
import random
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from achare import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True
    )

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
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

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    objects = UserManager()
    email = models.EmailField(
        unique=True,
        default=None
    )
    cellphone = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        default=None
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class BanCellphone(BaseModel):
    cellphone = models.CharField(
        max_length=11
    )
    number_of_try = models.IntegerField(default=0)
    ban_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.cellphone

    def is_ban(self):
        return bool(self.ban_time and self.ban_time > timezone.now())

    def ban(self):
        self.number_of_try = 0
        self.ban_time = timezone.now() + timezone.timedelta(minutes=settings.BAN_TIME_USER)
        self.save()


class BanIp(BaseModel):
    ip_address = models.GenericIPAddressField()
    number_of_try = models.IntegerField(default=0)
    ban_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ip_address

    def is_ban(self):
        return bool(self.ban_time and self.ban_time > timezone.now())

    def ban(self):
        self.number_of_try = 0
        self.ban_time = timezone.now() + timezone.timedelta(minutes=settings.BAN_TIME_USER)
        self.save()


class Authenticator(BaseModel):
    temp_token = models.UUIDField(
        default=uuid.uuid4,
    )
    cellphone = models.CharField(
        max_length=11,
    )
    sms_token = models.IntegerField(
        null=True,
        blank=True
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True
    )
    sms_verified = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.cellphone

    @property
    def is_valid_time(self):
        return timezone.now() <= self.expired_at

    @staticmethod
    def generate_verification_code():
        return random.randint(
            10 ** (settings.AUTHENTICATOR_CODE_LENGTH - 1),
            10 ** settings.AUTHENTICATOR_CODE_LENGTH
        )

    def send_verification_sms(self):
        self.sms_token = self.generate_verification_code()
        self.expired_at = datetime.datetime.now() + timezone.timedelta(minutes=settings.AUTHENTICATOR_CODE_EXPIRE_TIME)
        self.save()

    def verify_cellphone(self):
        self.sms_verified = True
        self.save()

    def can_verify_cellphone(self):
        return bool(
            not self.sms_verified and
            not self.complete and
            self.is_valid_time
        )

    def can_register(self):
        return bool(
            self.sms_verified and
            not self.complete
        )

    def register_user(self, first_name, last_name, password, email):
        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            cellphone=self.cellphone,
            password=password
        )
        self.complete = True
        self.save()

    def can_get_token(self):
        return self.complete


