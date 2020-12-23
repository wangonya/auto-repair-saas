import factory
from django.contrib.messages import get_messages
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
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Vehicle created.', messages[0])

    def test_post_new_vehicle_error(self):
        response = self.client.post(reverse('vehicles'), {})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Form is invalid.', messages[0])

    def test_update_vehicle(self):
        client = ContactFactory()
        vehicle = VehicleFactory()
        data = {
            'owner': client.id,
            'number_plate': fake.license_plate(),
        }
        response = self.client.post(
            reverse('update-vehicle', kwargs={'pk': vehicle.id}), data
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Vehicle updated.', messages[0])

    def test_delete_vehicle(self):
        vehicle = VehicleFactory()
        response = self.client.post(
            reverse('delete-vehicle', kwargs={'pk': vehicle.id})
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Vehicle deleted.', messages[0])

    def test_load_vehicles(self):
        client = ContactFactory()
        response = self.client.get(
            f'/vehicles/load-vehicles?client={client.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/vehicle_list_options.html')
        self.assertIsNotNone(response.context.get('vehicles'))
