from django.contrib.messages import get_messages
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.utils.factories import StaffFactory
from auto_repair_saas.apps.utils.tests import BaseTestCase

fake = Faker()


class StaffTestCase(BaseTestCase):
    def test_get_staff_page(self):
        response = self.client.get(reverse('staff'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_staff(self):
        data = {
            'name': 'customer',
            'staff_type': 'client'
        }
        response = self.client.post(reverse('staff'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Staff member created.', messages[0])

    def test_post_new_staff_error(self):
        response = self.client.post(reverse('staff'), {})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Form is invalid.', messages[0])

    def test_update_staff(self):
        staff = StaffFactory()
        data = {
            'name': fake.name(),
            'staff_type': 'client'
        }
        response = self.client.post(
            reverse('update-staff', kwargs={'pk': staff.id}), data
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Staff member updated.', messages[0])

    def test_delete_staff(self):
        staff = StaffFactory()
        response = self.client.post(
            reverse('delete-staff', kwargs={'pk': staff.id})
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Staff member deleted.', messages[0])

    def test_search_staff(self):
        staff_1 = StaffFactory()
        staff_2 = StaffFactory()

        response = self.client.get(
            f'/staff/search?q={staff_1.name}'
        )
        self.assertEqual(response.context['staff'].count(), 1)
        response = self.client.get(
            f'/staff/search?q={staff_2.email}'
        )
        self.assertEqual(response.context['staff'].count(), 1)
        response = self.client.get(f'/staff/search?q=')
        self.assertEqual(response.context['staff'].count(), 2)
