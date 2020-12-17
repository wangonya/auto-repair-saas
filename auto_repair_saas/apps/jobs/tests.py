from auto_repair_saas.apps.utils.tests import BaseTestCase


class JobsTestCase(BaseTestCase):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get('/jobs/')
        self.assertRedirects(response, '/auth/login?next=/jobs/')

    def test_get_jobs_page(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)
