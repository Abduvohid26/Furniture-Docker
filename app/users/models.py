from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from shared.models import BaseModel
from .utils import phone_regex, validate_image
from datetime import datetime, timedelta
from django.utils import timezone
from django.apps import apps
# from core.models import Order
ADMIN, MANAGER, WORKER, CHIEF, GUARD, OKLAD = ('admin', 'manager', 'worker', 'chief', 'guard', 'oklad')


class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
        (WORKER, WORKER),
        (CHIEF, CHIEF),
        (GUARD, GUARD),
        (OKLAD, OKLAD)
    )
    user_roles = models.CharField(max_length=100, choices=USER_ROLES, default=WORKER)
    phone_number = models.CharField(max_length=13, validators=[phone_regex])
    image = models.ImageField(upload_to='users-images/%Y/%m/%d/', default='default.svg', validators=[validate_image])
    filial_name = models.CharField(max_length=255, null=True, blank=True)
    salary_worker = models.IntegerField(default=0)
    monthly_earnings = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        access_token['user_roles'] = self.user_roles
        access_token['first_name'] = self.first_name
        access_token['username'] = self.username
        access_token['exp'] = int(access_token['exp'])
        return {
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }

    def check_hash_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.check_hash_password()
        super(User, self).save(*args, **kwargs)


class WorkStatics(BaseModel):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_static')
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name




