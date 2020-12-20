import factory
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.contacts.tests import ContactFactory
from auto_repair_saas.apps.utils.tests import BaseTestCase
from auto_repair_saas.apps.vehicles.models import Vehicle

fake = Faker()


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicle

    number_plate = fake.license_plate()
    owner = factory.SubFactory(ContactFactory)


class VehicleTestCase(BaseTestCase):
    def test_get_vehicles_page(self):
        response = self.client.get(reverse('vehicles'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_new_vehicle(self):
        client = ContactFactory()
        data = {
            'owner': client.id,
            'number_plate': fake.license_plate(),
        }
        response = self.client.post(reverse('vehicles'), data)
        self.assertIsNotNone(response.context['vehicles'])

    def test_post_new_vehicle_error(self):
        response = self.client.post(reverse('vehicles'), {})
        self.assertEqual(response.context['error'],
                         'Form is invalid.')
        self.assertIsNone(response.context.get('vehicles'))

    def test_load_vehicles(self):
        client = ContactFactory()
        response = self.client.get(f'/vehicles/load-vehicles?client={client.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/vehicle_list_options.html')
        self.assertIsNotNone(response.context.get('vehicles'))
