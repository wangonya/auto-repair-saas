import factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.authentication.models import User
from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.jobs.models import Job
from auto_repair_saas.apps.staff.models import Staff
from auto_repair_saas.apps.vehicles.models import Vehicle

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    email = fake.email()
    password = fake.password()


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    contact_type = 'client'
    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:20])


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicle

    number_plate = factory.LazyAttribute(lambda _: fake.license_plate())
    owner = factory.SubFactory(ContactFactory)


class StaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Staff

    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    client = factory.SubFactory(ContactFactory)
    vehicle = factory.SubFactory(VehicleFactory)
    charged = factory.LazyAttribute(lambda _: fake.random_int())
    due_start_date = factory.LazyAttribute(
        lambda _: fake.date_between(start_date='-1y', end_date='today')
    )
    due_end_date = factory.LazyAttribute(
        lambda _: fake.date_between(start_date='-1y', end_date='today')
    )
    assigned = factory.SubFactory(StaffFactory)
    status = factory.LazyAttribute(lambda _: fake.random_element(
        elements=('pending', 'confirmed', 'in_progress', 'done',)
    ))
    payment_method = factory.LazyAttribute(lambda _: fake.random_element(
        elements=('cash', 'card', 'mpesa',)
    ))
    paid = factory.LazyAttribute(lambda _: fake.random_element(
        elements=(True, False)
    ))
    payment_registered_on = factory.LazyAttribute(
        lambda _: fake.date_between(start_date='-1y', end_date='today')
    )


@login_required
def seed_data(request, *args, **kwargs):
    # clean tables
    for model in (Job, Staff, Vehicle, Contact,):
        model.objects.all().delete()

    for _ in range(0, 20):
        client = ContactFactory(contact_type='client')
        vehicle = VehicleFactory(owner=client)
        JobFactory(client=client, vehicle=vehicle)

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
