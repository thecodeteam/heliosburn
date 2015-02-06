import json
from django.test import TestCase
import subprocess
import logging
import time


class BaseTest(TestCase):
    def setUp(self):
        """
        Create temporary testserver.py and proxycore.py instances
        """
        logging.warning("Starting CherryPy server")
        self.django_process = subprocess.Popen(["/usr/bin/python2.7", "cherrypy_launcher.py"])  # TODO: fix this, obviously :)
        time.sleep(2)  # Let CherryPy begin listening

    def tearDown(self):
        """
        Tear down temporary testserver.py and proxycore.py instances
        """
        logging.warning("Killing CherryPy server")
        self.django_process.kill()


class RootTest(BaseTest):
    def test_root_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/webui/', target_status_code=302)


class WebuiRootTest(BaseTest):
    def test_webui_redirect(self):
        response = self.client.get('/webui/')
        self.assertRedirects(response, '/webui/signin?next=/webui/', target_status_code=301)

    def test_webui_url_fix_redirect(self):
        response = self.client.get('/webui/signin?next=/webui/')
        self.assertRedirects(response, '/webui/signin/?next=/webui/', status_code=301)


class SigninTest(BaseTest):
    def test_uses_template(self):
        response = self.client.get('/webui/signin/')
        self.assertTemplateUsed(response, 'signin.html')

    def test_incorrect_login(self):
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


class WebuiSignedInTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        response = self.client.post('/webui/signin/', {'username': 'admin', 'password': 'admin'})
        self.assertRedirects(response, 'webui/')


class SignoutTest(WebuiSignedInTest):
    def test_signout(self):
        # user is logged in
        response = self.client.get('/webui/')
        self.assertEqual(response.status_code, 200)

        # user logs out
        response = self.client.get('/webui/signout/')
        self.assertRedirects(response, '/webui/signin/')

        # user is logged out
        response = self.client.get('/webui/')
        self.assertNotEqual(response.status_code, 200)


class DashboardTest(WebuiSignedInTest):
    def test_dashboard_url_fix_redirect(self):
        response = self.client.get('/webui')
        self.assertRedirects(response, '/webui/', status_code=301)

    def test_uses_template(self):
        response = self.client.get('/webui/')
        self.assertTemplateUsed(response, 'dashboard.html')


class TrafficTest(WebuiSignedInTest):
    def test_traffic_status_code(self):
        response = self.client.get('/webui/ajax/traffic/')
        self.assertEqual(response.status_code, 200)

    def test_traffic_fields(self):
        response = self.client.get('/webui/ajax/traffic/')
        traffic_response = json.loads(response.content)

        self.assertIn('count', traffic_response)
        self.assertIn('requests', traffic_response)
