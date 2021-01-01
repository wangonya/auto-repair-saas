from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from ..contacts.models import Contact
from ..jobs.models import Job
from ..staff.models import Staff
from ..utils.factories import ContactFactory, JobFactory
from ..vehicles.models import Vehicle


@login_required
def seed_data(request, *args, **kwargs):
    # clean tables
    for model in (Job, Staff, Vehicle, Contact,):
        model.objects.all().delete()

    for _ in range(0, 20):
        JobFactory()
    for _ in range(0, 5):
        ContactFactory(contact_type='supplier')

    # cleanup estimates
    pending_estimates = Job.objects.filter(status='pending')
    for estimate in pending_estimates:
        estimate.paid = False
        estimate.payment_registered_on = None
        estimate.save()
    for job in Job.objects.all().exclude(status='pending'):
        if not job.paid:
            job.payment_registered_on = None
    return redirect(reverse('dashboard'))
