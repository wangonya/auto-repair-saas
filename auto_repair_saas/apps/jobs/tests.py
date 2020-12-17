from auto_repair_saas.apps.utils.tests import BaseTestCase


class JobsTestCase(BaseTestCase):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get('/jobs/')
        self.assertRedirects(response, '/auth/login?next=/jobs/')

    def test_get_jobs_page(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)

    def test_get_new_job_page(self):
        response = self.client.get('/jobs/new')
        self.assertEqual(response.status_code, 200)

    def test_post_new_job(self):
        data = {
            'client': 'customer',
            'vehicle': 'vehicle'
        }
        response = self.client.post('/jobs/new', data)
        self.assertRedirects(response, '/jobs/')
