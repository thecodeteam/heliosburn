from django.test import TestCase
import json
api_url = "http://127.0.0.1:8000/api"
admin_username = 'admin'
admin_password = 'admin'
test1_username = 'test1'
test1_password = 'test1'


class APITestCase(TestCase):
    """
    Subclass of Django's TestCase that includes login()
    """

    def login(self, username, password):
        """
        Login to HB API and store a valid X-AUTH-TOKEN.
        """
        r = self.client.post(path=api_url + "/auth/login",
                             data=json.dumps({'username': username, 'password': password}),
                             content_type="application/json")
        if 'x-auth-token' in r._headers:
            self.x_auth_token = r._headers['x-auth-token'][1]
            return True
        else:
            self.x_auth_token = None
            return False


class AuthViewTestCase(APITestCase):
    """
    Test views/auth.py
    """

    def test_login_admin(self):
        print("Testing LOGIN in %s" % self.__class__)
        login = self.login(admin_username, admin_password)
        self.assertTrue(login)

    def test_login_test1(self):
        login = self.login(test1_username, test1_password)
        self.assertTrue(login)


class SessionViewTestCase(APITestCase):
    """
    Test views/session.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for session model.
        """
        import json

        def create():
            self.login(admin_username, admin_password)
            body = json.dumps({
                'name': 'CRUD test',
                'description': 'CRUD test',
                'upstreamHost': '127.0.0.1',
                'upstreamPort': 8080,
                })

            response = self.client.post(path=api_url + "/session/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.session_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(api_url + "/session/" + self.session_id, HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

            self.login('test1', 'test1')
            response = self.client.get(api_url + "/session/" + self.session_id, HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

        def update():
            self.login(admin_username, admin_password)
            body = json.dumps({'name': 'CRUD test updated'})
            response = self.client.put(path=api_url + "/session/" + self.session_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

            self.login(test1_username, test1_password)
            response = self.client.put(path=api_url + "/session/" + self.session_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

        def delete():
            self.login(test1_username, test1_password)
            response = self.client.delete(path=api_url + "/session/" + self.session_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/session/" + self.session_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def linked_crud():
            # Create a testplan
            self.login(admin_username, admin_password)
            body = json.dumps({"name": "crud testplan"})
            response = self.client.post(path=api_url + "/testplan/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            testplan_id = json.loads(response.content)['id']

            # Create a session linked to testplan
            body = json.dumps({
                'name': 'crud session',
                'description': 'crud session description',
                'testplan': testplan_id,
                "upstreamHost": "127.0.0.1",
                "upstreamPort": 8080
            })
            response = self.client.post(path=api_url + "/session",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            session_id = json.loads(response.content)['id']

            # Delete session and testplan
            self.client.delete(path=api_url + "/session/" + session_id,
                               HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.client.delete(path=api_url + "/testplan/" + testplan_id,
                               HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()

        print("Testing CRUD specific to a linked testplan in %s" % self.__class__)
        linked_crud()


class TestplanViewTestCase(APITestCase):
    """
    Test views/testplan.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for testplan model.
        """
        import json

        def create():
            body = json.dumps({
                "name": "CRUD test with rule",
                "rules": [
                    {
                        'ruleType': 'request',
                        'name': 'test_rule_3',
                        'enabled': True,
                        'filter': {
                            'httpProtocol': 'HTTP/1.1',
                            'method': 'GET',
                            'headers': [
                                {'key': 'foo'},
                                {'key': 'fizz', 'value': 'buzz'},
                            ],
                        },
                        'action': {
                            'type': 'modify',
                            'method': 'PUT',
                            'url': 'www.newurl.com/foo/bar',
                            'setHeaders': [
                                {
                                    'key': 'zaphod', 'value': 'beeblebrox',
                                },
                            ],
                            'deleteHeaders': [
                                {
                                    'key': 'foo',
                                },
                            ],
                        }
                    },
                    ],
            })

            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/testplan/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.testplan_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/testplan/" + self.testplan_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            body = json.dumps({
                "name": "CRUD test with rule, name updated",
                "rules": [
                    {
                        'ruleType': 'request',
                        'filter': {
                            'httpProtocol': 'HTTP/1.1',
                            'method': 'GET',
                            'headers': [
                                {'key': 'paul bunyon'},
                                {'key': 'companion', 'value': 'blue oxe'},
                            ],
                        },
                        'action': {
                            'type': 'newResponse',
                            'httpProtocol': 'CARRIERPIGEON/1.1',
                            'statusCode': 403,
                            'statusDescription': 'TOO RIDICULOUS',
                            'headers': [
                                {
                                    'key': 'User-Agent',
                                    'value': 'Broken Telescope 1.9'
                                },
                            ],
                            'payload': 'The answer to life, the universe, and everything...is 42.',
                        }
                    },
                    ],
            })

            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/testplan/" + self.testplan_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/testplan/" + self.testplan_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


class UserViewTestCase(APITestCase):
    """
    Test views/user.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for user model.
        """
        import json

        def create():
            self.login(admin_username, admin_password)
            self.username = "crudtest"
            body = json.dumps({
                "username": self.username,
                "password": "CRUD test",
                "email": "test@test",
            })
            response = self.client.post(path=api_url + "/user/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)

            self.login(test1_username, test1_password)
            response = self.client.post(path=api_url + "/user/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/user/" + self.username,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

            response = self.client.get(path=api_url + "/user/",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

            self.login(test1_username, test1_password)
            response = self.client.get(path=api_url + "/user/",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

        def update():
            self.login(admin_username, admin_password)
            body = json.dumps({"email": "test1@test1"})
            response = self.client.put(path=api_url + "/user/" + self.username,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

            self.login(test1_username, test1_password)
            response = self.client.put(path=api_url + "/user/" + self.username,
                                     data=body,
                                     content_type="application/json",
                                     HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

        def delete():
            self.login(test1_username, test1_password)
            response = self.client.delete(path=api_url + "/user/" + self.username,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 403)

            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/user/" + self.username,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)


        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


class TrafficViewTestCase(APITestCase):
    """
    Test views/traffic.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for traffic model.
        """
        from models import snippet_generator

        def create():
            pass

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/traffic/",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            pass

        def delete():
            pass

        print("Generating test traffic in Redis")
        snippet_generator.generate_traffic()

        print("Testing READ in %s" % self.__class__)
        read()


class RuleViewTestCase(APITestCase):
    """
    Test views/rule.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for rule model.
        """
        import json

        def create():
            body = json.dumps({
                'ruleType': 'request',
                'name': 'test_rule_2',
                'enabled': True,
                'filter': {
                    'httpProtocol': 'HTTP/1.1',
                    'method': 'GET',
                    'headers': [
                        {'key': 'foo'},
                        {'key': 'fizz', 'value': 'buzz'},
                    ],
                },
                'action': {
                    'type': 'modify',
                    'method': 'PUT',
                    'url': 'www.newurl.com/foo/bar',
                    'setHeaders': [
                        {
                            'key': 'zaphod', 'value': 'beeblebrox',
                        },
                    ],
                    'deleteHeaders': [
                        {
                            'key': 'foo',
                        },
                    ],
                }
            })
            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/rule/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.rule_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/rule/" + self.rule_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            body = json.dumps({
                'ruleType': 'request',
                'enabled': True,
                'name': 'test_rule_4',
                'filter': {
                    'httpProtocol': 'HTTP/1.1',
                    'method': 'GET',
                    'headers': [
                        {'key': 'paul bunyon'},
                        {'key': 'companion', 'value': 'blue oxe'},
                    ],
                },
                'action': {
                    'type': 'newResponse',
                    'httpProtocol': 'CARRIERPIGEON/1.1',
                    'statusCode': 403,
                    'statusDescription': 'TOO RIDICULOUS',
                    'headers': [
                        {
                            'key': 'User-Agent',
                            'value': 'Broken Telescope 1.9'
                        },
                    ],
                    'payload': 'The answer to life, the universe, and everything...is 42.',
                },
            })
            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/rule/" + self.rule_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/rule/" + self.rule_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)


        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


class TestplanRuleViewTestCase(APITestCase):
    """
    Test views/testplan_rule.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for testplan model.
        """
        import json

        def create_testplan():
            self.login(admin_username, admin_password)
            body = json.dumps({"name": "CRUD test for testplan_rule"})
            response = self.client.post(path=api_url + "/testplan/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.testplan_id = in_json['id']

        def delete_testplan():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/testplan/" + self.testplan_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def create():
            body = json.dumps({
                'ruleType': 'request',
                'enabled': True,
                'name': 'test_rule_1',
                'filter': {
                    'httpProtocol': 'HTTP/1.1',
                    'method': 'GET',
                    'headers': [
                        {'key': 'foo'},
                        {'key': 'fizz', 'value': 'buzz'},
                    ],
                },
                'action': {
                    'type': 'modify',
                    'method': 'PUT',
                    'url': 'www.newurl.com/foo/bar',
                    'setHeaders': [
                        {
                            'key': 'zaphod', 'value': 'beeblebrox',
                        },
                    ],
                    'deleteHeaders': [
                        {
                            'key': 'foo',
                        },
                    ],
                }
            })
            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/testplan/" + self.testplan_id + "/rule/",
                                     data=body,
                                     content_type="application/json",
                                     HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            return in_json['id']

        def read(rule_id):
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/testplan/" + self.testplan_id + "/rule/" + rule_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update(rule_id):
            body = json.dumps({
                'ruleType': 'request',
                'enabled': True,
                'name': 'test_rule_4',
                'filter': {
                    'httpProtocol': 'HTTP/1.1',
                    'method': 'GET',
                    'headers': [
                        {'key': 'folk hero'},
                        {'key': 'instrument', 'value': 'violin'},
                    ],
                },
                'action': {
                    'type': 'newResponse',
                    'httpProtocol': 'CARRIERFLAMINGO/1.1',
                    'statusCode': 403,
                    'statusDescription': 'TOO FEATHERY',
                    'headers': [
                        {
                            'key': 'User-Agent',
                            'value': 'Broken Looking Glass 1.9'
                        },
                    ],
                    'payload': 'The answer to life, the universe, and everything...is----NO CARRIER.',
                }

            })
            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/testplan/" + self.testplan_id + "/rule/" + rule_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete(rule_id):
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/testplan/" + self.testplan_id + "/rule/" + rule_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Creating temporary testplan for use within %s" % self.__class__)
        create_testplan()

        print("Testing CREATE #1 in %s" % self.__class__)
        rule1_id = create()

        print("Testing CREATE #2 in %s" % self.__class__)
        rule2_id = create()

        print("Testing READ in %s" % self.__class__)
        read(rule1_id)

        print("Testing UPDATE in %s" % self.__class__)
        update(rule1_id)

        print("Testing DELETE #1 in %s" % self.__class__)
        delete(rule1_id)

        print("Testing DELETE #2 in %s" % self.__class__)
        delete(rule2_id)

        print("Removing temporary testplan for use within %s" % self.__class__)
        delete_testplan()


class RecordingViewTestCase(APITestCase):
    """
    Test views/recording.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for recording model.
        """
        import json

        def create():
            body = json.dumps({
                "name": "CRUD test for recording",
            })
            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/recording/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)

            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.recording_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/recording/" + self.recording_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            body = json.dumps({
                "name": "CRUD test for recording, updated",
                "description": "description...",
            })
            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/recording/" + self.recording_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/recording/" + self.recording_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()

class QOSViewTestCase(APITestCase):
    """
    Test views/qos.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for qos model.
        """
        import json

        def create():
            body = json.dumps({
                "latency": 100,
                "name": "test QOS profile",
                "description": "unit test QOS profile",
                "jitter": {
                    "min": 10,
                    "max": 50
                },
                "trafficLoss": 0.1
            })
            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/qos/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)

            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.qos_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/qos/" + self.qos_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            body = json.dumps({
                "name": "renamed unit test QOS profile",
                "latency": 500
            })
            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/qos/" + self.qos_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/qos/" + self.qos_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


class ServerOverloadViewTestCase(APITestCase):
    """
    Test views/serveroverload.py CRUD
    """

    def test_crud(self):
        """
        Tests CRUD for server overload model.
        """
        import json

        def create():
            self.profile = {
                'name': 'test profile',
                'description': 'test description',
                'function': {
                    'type': 'test type',
                    'expValue': 1,
                    'growthRate': 1,
                },
                'response_triggers': [
                    {
                        'fromLoad': 1,
                        'toLoad': 1,
                        'actions': [
                            {
                                'type': 'response',
                                'value': '503',
                                'percentage': 0.3,
                            },
                        ],
                    },
                ],
            }
            body = json.dumps(self.profile)
            self.login(admin_username, admin_password)
            response = self.client.post(path=api_url + "/serveroverload/",
                                        data=body,
                                        content_type="application/json",
                                        HTTP_X_AUTH_TOKEN=self.x_auth_token)

            self.assertEqual(response.status_code, 200)
            self.assertIn("location", response._headers)
            in_json = json.loads(response.content)
            self.assertIn("id", in_json)
            self.serveroverload_id = in_json['id']

        def read():
            self.login(admin_username, admin_password)
            response = self.client.get(path=api_url + "/serveroverload/" + self.serveroverload_id,
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def update():
            self.profile['name'] = 'updated name'
            body = json.dumps(self.profile)
            self.login(admin_username, admin_password)
            response = self.client.put(path=api_url + "/serveroverload/" + self.serveroverload_id,
                                       data=body,
                                       content_type="application/json",
                                       HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        def delete():
            self.login(admin_username, admin_password)
            response = self.client.delete(path=api_url + "/serveroverload/" + self.serveroverload_id,
                                          HTTP_X_AUTH_TOKEN=self.x_auth_token)
            self.assertEqual(response.status_code, 200)

        print("Testing CREATE in %s" % self.__class__)
        create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


class LogTestCase(APITestCase):
    """
    Test log retrieval.
    """

    def test_log_get(self):
        self.login(admin_username, admin_password)
        response = self.client.get(path=api_url + "/log/",
                                   HTTP_X_AUTH_TOKEN=self.x_auth_token)
        pass
