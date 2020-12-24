from django.contrib.messages import get_messages
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.utils.factories import ContactFactory
from auto_repair_saas.apps.utils.tests import BaseTestCase

fake = Faker()


class ContactsTestCase(BaseTestCase):
    def test_get_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_contact(self):
        data = {
            'name': 'customer',
            'contact_type': 'client'
        }
        response = self.client.post(reverse('contacts'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Contact created.', messages[0])

    def test_post_new_contact_error(self):
        response = self.client.post(reverse('contacts'), {})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Form is invalid.', messages[0])

    def test_update_contact(self):
        contact = ContactFactory()
        data = {
            'name': fake.name(),
            'contact_type': 'client'
        }
        response = self.client.post(
            reverse('update-contact', kwargs={'pk': contact.id}), data
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Contact updated.', messages[0])

    def test_delete_contact(self):
        contact = ContactFactory()
        response = self.client.post(
            reverse('delete-contact', kwargs={'pk': contact.id})
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertEqual('Contact deleted.', messages[0])
