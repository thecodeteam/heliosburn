import json
from django.test import TestCase


class RootTest(TestCase):
    def test_root_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/webui/', target_status_code=302)


class WebuiRootTest(TestCase):
    def test_webui_redirect(self):
        response = self.client.get('/webui/')
        self.assertRedirects(response, '/webui/signin?next=/webui/', target_status_code=301)

    def test_webui_url_fix_redirect(self):
        response = self.client.get('/webui/signin?next=/webui/')
        self.assertRedirects(response, '/webui/signin/?next=/webui/', status_code=301)


class SigninTest(TestCase):
    def test_uses_template(self):
        response = self.client.get('/webui/signin/')
        self.assertTemplateUsed(response, 'signin.html')

    def test_form_fields(self):
        response = self.client.post('/webui/signin/', {'username': 'fake_user', 'password': 'fake_password'})
        self.assertEqual(response.status_code, 200)
        m = list(response.context['messages'])
        self.assertEqual(len(m), 1)
        self.assertEqual(str(m[0]), 'Invalid login credentials')

    def test_correct_login(self):
        response = self.client.post('/webui/signin/', {'username': 'admin', 'password': 'admin'})
        self.assertRedirects(response, 'webui/')

    def test_correct_login_custom_redirect(self):
        response = self.client.post('/webui/signin/?next=/webui/testplans/', {'username': 'admin', 'password': 'admin'})
        self.assertRedirects(response, 'webui/testplans/')


class WebuiSignedInTest(TestCase):
    def setUp(self):
        self.client.post('/webui/signin/', {'username': 'admin', 'password': 'admin'})


class DashboardTest(WebuiSignedInTest):
    def test_dashboard_url_fix_redirect(self):
        response = self.client.get('/webui')
        self.assertRedirects(response, '/webui/', status_code=301)


class TrafficTest(WebuiSignedInTest):
    def test_traffic_status_code(self):
        response = self.client.get('/webui/ajax/traffic/')
        self.assertEqual(response.status_code, 200)

    def test_traffic_fields(self):
        response = self.client.get('/webui/ajax/traffic/')
        traffic_response = json.loads(response.content)

        self.assertIn('count', traffic_response)
        self.assertIn('requests', traffic_response)
