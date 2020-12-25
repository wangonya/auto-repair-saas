from django.db import models

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.staff.models import Staff
from auto_repair_saas.apps.vehicles.models import Vehicle


class Job(models.Model):
    class Meta:
        ordering = ('-created_on',)

    job_status_choices = (('pending', 'Pending'),
                          ('confirmed', 'Confirmed'),
                          ('in_progress', 'In progress'),
                          ('done', 'Done'))
    client = models.ForeignKey(Contact, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    due_start_date = models.DateField(null=True, blank=True)
    due_end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assigned = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    charged = models.FloatField(null=True, blank=True, default=0)
    status = models.CharField(
        choices=job_status_choices, max_length=15, null=False, blank=False,
        default='pending',
    )
