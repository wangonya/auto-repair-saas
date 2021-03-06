from django.db import models

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.utils.models import BaseModel, ModelManager


class Vehicle(BaseModel):
    class Meta:
        ordering = ('owner__name',)

    number_plate = models.CharField(max_length=15)
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.number_plate

    objects = ModelManager()
