from auto_repair_saas.apps.utils.tests import BaseTestCase


class ContactsTestCase(BaseTestCase):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get('/contacts/')
        self.assertRedirects(response, '/auth/login?next=/contacts/')

    def test_get_contacts_page(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_get_new_contact_page(self):
        response = self.client.get('/contacts/new')
        self.assertEqual(response.status_code, 200)

    def test_post_new_contact(self):
        data = {
            'name': 'customer',
            'contact_type': 'client'
        }
        response = self.client.post('/contacts/new', data)
        self.assertRedirects(response, '/contacts/')

    def test_post_new_contact_error(self):
        response = self.client.post('/contacts/new', {})
        self.assertEqual(response.context['error'],
                         'Form is invalid.')
