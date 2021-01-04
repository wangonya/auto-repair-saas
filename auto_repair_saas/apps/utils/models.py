from datetime import datetime

from django.conf import settings
from django.db import models

from auto_repair_saas.apps.utils.middleware import \
    CurrentUserMiddleware


def get_current_user():
    return CurrentUserMiddleware.get_current_user()


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        db_index=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Created by',
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL
    )
    last_modified_at = models.DateTimeField(
        'Last modified at',
        auto_now=True,
        db_index=True
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Last modified by',
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_last_modified",
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def set_user_fields(self, user):
        """
        Set user-related fields before saving the instance.
        If no user with a primary key is given the fields are not
        set.
        """
        if user and user.pk:
            if not self.pk:
                self.created_by = user
            self.last_modified_by = user

    def save(self, *args, **kwargs):
        self.last_modified_at = datetime.now()
        current_user = get_current_user()
        self.set_user_fields(current_user)
        super(BaseModel, self).save(*args, **kwargs)


class ModelManager(models.Manager):
    """filters queries to always return data belonging to current user"""

    def get_queryset(self):
        try:
            return super(ModelManager, self).get_queryset().filter(
                created_by=get_current_user()
            )
        except TypeError:
            # user not logged in
            pass

    def get_object(self):
        try:
            return super(ModelManager, self).get_object().filter(
                created_by=get_current_user()
            )
        except TypeError:
            # user not logged in
            pass
