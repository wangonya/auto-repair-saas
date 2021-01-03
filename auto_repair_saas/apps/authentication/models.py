from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not (email and username and password):
            raise ValidationError(
                'Name, email, and password are required to create a user.'
            )
        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username, **extra_fields
        )
        user.set_password(password)
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email


def send_welcome_message(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome aboard!',
            'Thanks for trying the auto repair shop management app.',
            'kwangonya@gmail.com',
            [instance.email],
            fail_silently=False,
        )


post_save.connect(send_welcome_message, sender=User)
