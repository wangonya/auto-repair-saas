from django.db import models

from auto_repair_saas.apps.contacts.models import Contact


class Vehicle(models.Model):
    number_plate = models.CharField(max_length=15)
    owner = models.ForeignKey(Contact, on_delete=models.RESTRICT)
    created_on = models.DateTimeField(auto_now_add=True)
