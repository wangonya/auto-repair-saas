from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from ..utils.factories import ContactFactory, JobFactory


@login_required
def seed_data(request, *args, **kwargs):
    for _ in range(0, 15):
        JobFactory()
    for _ in range(0, 5):
        ContactFactory(contact_type='supplier')
    return redirect(reverse('dashboard'))
