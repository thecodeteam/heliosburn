import json
import re
from django.test import TestCase
import subprocess
import logging
import time
import uuid
from webui.forms import TestPlanForm


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create temporary testserver.py and proxycore.py instances
        """
        logging.warning("Starting CherryPy server")
        cls.django_process = subprocess.Popen(["/usr/bin/python2.7", "cherrypy_launcher.py"])  # TODO: fix this, obviously :)
        time.sleep(2)  # Let CherryPy begin listening

    @classmethod
    def tearDownClass(cls):
        """
        Tear down temporary testserver.py and proxycore.py instances
        """
        logging.warning("Killing CherryPy server")
        cls.django_process.kill()


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


class TestPlanTest(WebuiSignedInTest):
    def test_testplan_url_fix_redirect(self):
        response = self.client.get('/webui/testplans')
        self.assertRedirects(response, '/webui/testplans/', status_code=301)

    def test_testplan_list_uses_template(self):
        response = self.client.get('/webui/testplans/')
        self.assertTemplateUsed(response, 'testplan/testplan_list.html')

    def test_testplan_list_status_code(self):
        response = self.client.get('/webui/testplans/')
        self.assertEqual(response.status_code, 200)

    def test_testplan_new_uses_template(self):
        response = self.client.get('/webui/testplans/new/')
        self.assertTemplateUsed(response, 'testplan/testplan_new.html')

    def test_testplan_new_status_code(self):
        response = self.client.get('/webui/testplans/new/')
        self.assertEqual(response.status_code, 200)

    def test_testplan_new_form_missing_required_fields(self):
        form_data = {}
        form_data['description'] = 'Description...'
        form_data['latencyEnabled'] = True
        form_data['clientLatency'] = 0
        form_data['serverLatency'] = 100
        form = TestPlanForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_testplan_new_form_valid_all_fields(self):
        form_data = {}
        form_data['name'] = 'Test Plan %s' % (uuid.uuid4().hex,)
        form_data['description'] = 'Description...'
        form_data['latencyEnabled'] = True
        form_data['clientLatency'] = 0
        form_data['serverLatency'] = 100
        form = TestPlanForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_testplan_new_form_valid_minimal_fields(self):
        form_data = {}
        form_data['name'] = 'Test Plan %s' % (uuid.uuid4().hex,)
        form_data['description'] = 'Description...'
        form = TestPlanForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_testplan_submit_missing_fields(self):
        form_data = {}
        form_data['description'] = 'Description...'
        form_data['latencyEnabled'] = True
        form_data['clientLatency'] = 0
        form_data['serverLatency'] = 100
        response = self.client.post('/webui/testplans/new/', form_data)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_testplan_submit_valid_fields(self):
        form_data = {}
        form_data['name'] = 'Test Plan %s' % (uuid.uuid4().hex,)
        form_data['description'] = 'Description...'
        form_data['latencyEnabled'] = True
        form_data['clientLatency'] = 0
        form_data['serverLatency'] = 100

        response = self.client.post('/webui/testplans/new/', form_data)

        location = response.url
        pattern = '.+testplans\/(?P<id>\w+)'
        p = re.compile(pattern)
        m = p.match(location)
        testplan_id = m.group('id')
        self.assertRedirects(response, '/webui/testplans/%s' % (testplan_id,))

    def test_testplan_details_invalid_id(self):
        response = self.client.get('/webui/testplans/9999999')
        self.assertTemplateUsed(response, '404.html')

    def test_testplan_details_valid_id(self):
        response = self.client.get('/webui/testplans/1')
        self.assertEqual(response.status_code, 200)

    def test_testplan_delete_invalid(self):
        data = {}
        data['testplans'] = [99999996, 99999997, 99999998, 99999999]
        response = self.client.post('/webui/testplans/delete/', data)
        self.assertEqual(response.status_code, 404)

    def test_testplan_delete_invalid(self):
        data = {}
        data['testplans'] = [99999996, 99999997, 99999998, 99999999]
        response = self.client.post('/webui/testplans/delete/', data)
        self.assertEqual(response.status_code, 404)

    def test_testplan_delete_valid(self):
        form_data = {}
        form_data['name'] = 'Test Plan %s' % (uuid.uuid4().hex,)
        form_data['description'] = 'Description...'
        form_data['latencyEnabled'] = True
        form_data['clientLatency'] = 0
        form_data['serverLatency'] = 100

        response = self.client.post('/webui/testplans/new/', form_data)

        location = response.url
        pattern = '.+testplans\/(?P<id>\w+)'
        p = re.compile(pattern)
        m = p.match(location)
        testplan_id = m.group('id')
        self.assertRedirects(response, '/webui/testplans/%s' % (testplan_id,))

        data = {}
        data['testplans'] = [testplan_id]
        response = self.client.post('/webui/testplans/delete/', data)
        self.assertEqual(response.status_code, 200)


class RecordingTest(WebuiSignedInTest):
    def test_recording_url_fix_redirect(self):
        response = self.client.get('/webui/recordings')
        self.assertRedirects(response, '/webui/recordings/', status_code=301)

    def test_recording_list_uses_template(self):
        response = self.client.get('/webui/recordings/')
        self.assertTemplateUsed(response, 'recording/recording_list.html')