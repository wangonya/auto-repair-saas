from django.urls import reverse

from auto_repair_saas.apps.utils.tests import BaseTestCase


class DashboardTestCase(BaseTestCase):
    def test_get_dashboard_page(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_get_dashboard_data(self):
        response = self.client.get(reverse('dashboard-data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('sales'), 0)
