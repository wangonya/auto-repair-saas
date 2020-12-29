from django.contrib.messages import get_messages
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.contacts.tests import ContactFactory
from auto_repair_saas.apps.utils.factories import JobFactory
from auto_repair_saas.apps.utils.tests import BaseTestCase
from auto_repair_saas.apps.vehicles.tests import VehicleFactory

fake = Faker()


class JobsTestCase(BaseTestCase):
    def test_get_jobs_page(self):
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_job(self):
        client = ContactFactory()
        vehicle = VehicleFactory(owner=client)
        data = {
            'client': client.id,
            'vehicle': vehicle.id,
            'charged': fake.random_int(),
            'payment_method': 'cash',
            'status': 'pending'
        }
        response = self.client.post(reverse('jobs'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Job created.', messages[0])

    def test_post_new_job_error(self):
        response = self.client.post(reverse('jobs'), {})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Form is invalid.', messages[0])

    def test_update_job(self):
        job = JobFactory()
        data = {
            'client': job.client_id,
            'vehicle': job.vehicle_id,
            'charged': job.charged + 1,
            'assigned': job.assigned_id,
            'payment_method': 'cash',
            'status': 'pending'
        }
        response = self.client.post(
            reverse('update-job', kwargs={'pk': job.id}), data
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Job updated.', messages[0])

    def test_delete_job(self):
        job = JobFactory()
        response = self.client.post(
            reverse('delete-job', kwargs={'pk': job.id})
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Job deleted.', messages[0])

    def test_search_job(self):
        job_1 = JobFactory()
        job_2 = JobFactory()

        def get_job_status_count(job):
            count = ''
            status = job.status
            if status in ('pending', 'confirmed',):
                count = 'estimates_count'
            elif status == 'in_progress':
                count = 'in_progress_count'
            elif status == 'done':
                count = 'done_count'
            return count

        response = self.client.get(f'/jobs/search?q={job_1.client.name}')
        self.assertEqual(response.context[get_job_status_count(job_1)], 1)
        response = self.client.get(f'/jobs/search?q={job_2.client.name}')
        self.assertEqual(response.context[get_job_status_count(job_2)], 1)

    def test_register_payment(self):
        job = JobFactory(paid=False, charged=5000)
        response = self.client.post(
            reverse('pay-job', kwargs={'pk': job.id}),
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Payment registered.', messages[0])
