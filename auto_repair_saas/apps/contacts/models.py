from django.db import models

from auto_repair_saas.apps.utils.models import BaseModel, ModelManager


class Contact(BaseModel):
    CONTACT_TYPE_CHOICES = (
        ('client', 'Client'), ('supplier', 'Supplier'))
    contact_type = models.CharField(
        choices=CONTACT_TYPE_CHOICES, max_length=8, null=False, blank=False,
        db_index=True
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = ModelManager()
