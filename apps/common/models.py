import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.common.managers import CustomUserManager
from helpers.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    _validate_phone = RegexValidator(
        regex=r"^998\d{9}$",
        message='Phone number must start from 998 and contain 9 characters. For example: 998998065999'
    )
    username = None
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=12, validators=[_validate_phone], null=True)

    USERNAME_FIELD = "name"
    objects = CustomUserManager()

    def __str__(self):
        return self.name
