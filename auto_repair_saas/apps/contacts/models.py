from django.db import models


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = (
        ('client', 'Client'), ('supplier', 'Supplier'))
    contact_type = models.CharField(
        choices=CONTACT_TYPE_CHOICES, max_length=8, null=False, blank=False,
        db_index=True
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
