import factory
from django.urls import reverse
from faker import Faker

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.utils.tests import BaseTestCase

fake = Faker()


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    contact_type = 'client'
    name = fake.name()


class ContactsTestCase(BaseTestCase):
    def test_get_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_get_new_contact_page(self):
        response = self.client.get(reverse('new-contact'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_contact(self):
        data = {
            'name': 'customer',
            'contact_type': 'client'
        }
        response = self.client.post(reverse('new-contact'), data)
        self.assertRedirects(response, reverse('contacts'))

    def test_post_new_contact_error(self):
        response = self.client.post(reverse('new-contact'), {})
        self.assertEqual(response.context['error'],
                         'Form is invalid.')
