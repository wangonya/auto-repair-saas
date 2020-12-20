import random
import string
import sys

from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import date


class UserManager(BaseUserManager):
    @staticmethod
    def generate_tenant_schema_name():
        letters = string.ascii_lowercase
        schema_name = ''.join(random.choice(letters) for _ in range(20))
        return schema_name

    def create_user(self, username, email, password, **extra_fields):
        if not (email and username and password):
            raise ValidationError(
                'Name, email, and password are required to create a user.'
            )
        schema_name = self.generate_tenant_schema_name()
        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username, schema=schema_name, **extra_fields
        )
        user.set_password(password)
        user.save()

        if 'test' not in sys.argv:  # don't create tenants for tests
            from auto_repair_saas.apps.tenants.create_tenant import create_tenant  # noqa
            create_tenant(schema_name=user.schema,
                          paid_until=date.today() + relativedelta(months=+1),
                          on_trial=True)

        return user


class User(AbstractUser):
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)
    schema = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email
