from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.contacts.tests import ContactFactory
from auto_repair_saas.apps.utils.tests import BaseTestCase
from auto_repair_saas.apps.vehicles.tests import VehicleFactory

fake = Faker()

class JobsTestCase(BaseTestCase):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('jobs'))
        self.assertRedirects(response, '/auth/login?next=/jobs/')

    def test_get_jobs_page(self):
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)

    def test_get_new_job_page(self):
        response = self.client.get(reverse('new-job'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_job(self):
        client = ContactFactory()
        vehicle = VehicleFactory(owner=client)
        data = {
            'client': client.id,
            'vehicle': vehicle.id,
            'charged': fake.random_int()
        }
        response = self.client.post(reverse('new-job'), data)
        self.assertRedirects(response, reverse('jobs'))

    def test_post_new_job_error(self):
        response = self.client.post(reverse('new-job'), {})
        self.assertEqual(response.context['error'],
                         'Form is invalid.')
