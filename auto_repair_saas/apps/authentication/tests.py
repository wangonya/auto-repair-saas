import factory
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import signals
from django.test import TestCase
from faker import Faker

from .models import User

fake = Faker()


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    email = fake.email()
    password = fake.password()


class AuthTestCase(TestCase):
    def test_get_user_registration_page(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        username = 'test'
        email = 'test@mail.com'
        password = 'Testuser123'
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(email=email)
        data = {
            'name': username,
            'email': email,
            'password': password
        }
        response = self.client.post(
            '/auth/register', data=data
        )
        self.assertTrue(User.objects.get(email=email))
        self.assertIn(email, response.context['success'])

    def test_user_cannot_register_with_existing_email(self):
        user = UserFactory()
        data = {
            'name': user.username,
            'email': user.email,
            'password': user.password
        }
        response = self.client.post(
            '/auth/register', data=data
        )
        self.assertEqual(response.context['error'],
                         'An account with that email already exists.')

    def test_details_required_to_register_user(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='', email='', password='')

    def test_get_user_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_existing_user_can_login(self):
        with factory.django.mute_signals(signals.post_save):
            self.test_user_can_register()
        data = {
            'email': 'test@mail.com',
            'password': 'Testuser123'
        }
        response = self.client.post(
            '/auth/login', data=data
        )
        # self.assertRedirects(response, '/auth/register/success')

    def test_user_cannot_login_with_invalid_credentials(self):
        email = 'test123@mail.com'
        password = 'Testuser12345'

        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(
            '/auth/login', data=data
        )
        self.assertEqual(response.context['error'],
                         'Invalid email / password.')
