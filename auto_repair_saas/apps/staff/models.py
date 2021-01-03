from django.db import models

from auto_repair_saas.apps.utils.models import BaseModel, ModelManager


class Staff(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = ModelManager()
