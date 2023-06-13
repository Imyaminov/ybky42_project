import uuid
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from helpers.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    _validate_phone = RegexValidator(
        regex=r"^998\d{9}$",
        message='Phone number must start from 998 and contain 9 characters. For example: 998998065999'
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=12, unique=True, validators=[_validate_phone], null=True)
    email = models.EmailField(unique=True, null=True)
    is_moderator = models.BooleanField(default=False, verbose_name="Moderator")

    objects = UserManager()

    def __str__(self):
        return self.username
