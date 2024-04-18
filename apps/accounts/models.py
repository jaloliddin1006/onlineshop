import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from apps.base.models import BaseModel


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', default='default/user.png', blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username
    

EMAIL_EXPIRE_TIME = 5


class UserResetPasswordCode(BaseModel):
    private_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    expiration_time = models.DateTimeField(null=True, blank=True)
    is_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        return super(UserResetPasswordCode, self).save(*args, **kwargs)
