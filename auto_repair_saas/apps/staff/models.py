from django.db import models


class Staff(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
