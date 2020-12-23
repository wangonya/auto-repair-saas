import factory
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from .models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    email = fake.email()
    password = fake.password()


class AuthTestCase(TestCase):
    def test_get_user_registration_page(self):
        response = self.client.get(reverse('register'))
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
            reverse('register'), data=data
        )
        self.assertTrue(User.objects.get(email=email))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(len(messages) == 1)
        self.assertIn(email, messages[0])

    def test_user_cannot_register_with_existing_email(self):
        user = UserFactory()
        data = {
            'name': user.username,
            'email': user.email,
            'password': user.password
        }
        response = self.client.post(
            reverse('register'), data=data
        )
        self.assertEqual(response.context['error'],
                         'An account with that email already exists.')

    def test_details_required_to_register_user(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(username='', email='', password='')

    def test_get_user_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_existing_user_can_login(self):
        self.test_user_can_register()
        data = {
            'username': 'test@mail.com',
            'password': 'Testuser123'
        }
        response = self.client.post(
            reverse('login'), data=data
        )
        self.assertRedirects(response, reverse('dashboard'))
