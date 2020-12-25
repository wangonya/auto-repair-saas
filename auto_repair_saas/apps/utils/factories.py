import factory
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
        lambda _: fake.date_between(start_date='today', end_date='+1w')
    )
    due_end_date = factory.LazyAttribute(
        lambda _: fake.date_between(start_date='+1w', end_date='+4w')
    )
    assigned = factory.SubFactory(StaffFactory)
    status = factory.LazyAttribute(lambda _: fake.random_element(
        elements=('pending', 'confirmed', 'in_progress', 'done',)
    ))
