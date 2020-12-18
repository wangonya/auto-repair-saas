from django.test import TestCase

from auto_repair_saas.apps.authentication.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@mail.com', 'Test123!')
        self.client.force_login(user)
