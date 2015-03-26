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
        from views import session, testplan

        def create():
            self.login(admin_username, admin_password)
            body = json.dumps({
                'name': 'CRUD test',
                'description': 'CRUD test',
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
        username = create()

        print("Testing READ in %s" % self.__class__)
        read()

        print("Testing UPDATE in %s" % self.__class__)
        update()

        print("Testing DELETE in %s" % self.__class__)
        delete()


# class TrafficViewTestCase(TestCase):
#     """
#     Test views/traffic.py CRUD
#     This test requires a valid user "admin" with password "admin".
#     """
#
#     def test_crud(self):
#         """
#         Tests CRUD for traffic model.
#         """
#         from views import traffic
#         from models import snippet_generator
#
#         def create(request):
#             pass
#
#         def read(request):
#             response = traffic.get(request)
#             self.assertEqual(response.status_code, 200)
#
#         def update(request, username):
#             pass
#
#         def delete(request, username):
#             pass
#
#         print("Creating authenticated request for CRUD tests in %s" % self.__class__)
#         request = create_authenticated_request("admin", "admin")
#         request.method = "POST"
#
#         print("Generating test traffic in Redis")
#         snippet_generator.generate_traffic()
#
#         print("Testing READ in %s" % self.__class__)
#         read(request)
#
#
# class RuleViewTestCase(TestCase):
#     """
#     Test views/rule.py CRUD
#     This test requires a valid user "admin" with password "admin".
#     """
#
#     def test_crud(self):
#         """
#         Tests CRUD for rule model.
#         """
#         from views import rule
#         import json
#
#         def create(request):
#             request.body = json.dumps({
#                 'ruleType': 'request',
#                 'name': 'test_rule_2',
#                 'enabled': True,
#                 'filter': {
#                     'httpProtocol': 'HTTP/1.1',
#                     'method': 'GET',
#                     'headers': [
#                         {'key': 'foo'},
#                         {'key': 'fizz', 'value': 'buzz'},
#                     ],
#                 },
#                 'action': {
#                     'type': 'modify',
#                     'method': 'PUT',
#                     'url': 'www.newurl.com/foo/bar',
#                     'setHeaders': [
#                         {
#                             'key': 'zaphod', 'value': 'beeblebrox',
#                         },
#                     ],
#                     'deleteHeaders': [
#                         {
#                             'key': 'foo',
#                         },
#                     ],
#                 }
#             })
#             response = rule.post(request)
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("location", response._headers)
#             in_json = json.loads(response.content)
#             self.assertIn("id", in_json)
#             return in_json['id']
#
#         def read(request, rule_id):
#             response = rule.get(request, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         def update(request, rule_id):
#             request.body = json.dumps({
#                 'ruleType': 'request',
#                 'enabled': True,
#                 'name': 'test_rule_4',
#                 'filter': {
#                     'httpProtocol': 'HTTP/1.1',
#                     'method': 'GET',
#                     'headers': [
#                         {'key': 'paul bunyon'},
#                         {'key': 'companion', 'value': 'blue oxe'},
#                     ],
#                 },
#                 'action': {
#                     'type': 'newResponse',
#                     'httpProtocol': 'CARRIERPIGEON/1.1',
#                     'statusCode': 403,
#                     'statusDescription': 'TOO RIDICULOUS',
#                     'headers': [
#                         {
#                             'key': 'User-Agent',
#                             'value': 'Broken Telescope 1.9'
#                         },
#                     ],
#                     'payload': 'The answer to life, the universe, and everything...is 42.',
#                 },
#             })
#             response = rule.put(request, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         def delete(request, rule_id):
#             response = rule.delete(request, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         print("Creating authenticated request for CRUD tests in %s" % self.__class__)
#         request = create_authenticated_request("admin", "admin")
#         request.method = "POST"
#
#         print("Testing CREATE in %s" % self.__class__)
#         rule_id = create(request)
#
#         print("Testing READ in %s" % self.__class__)
#         read(request, rule_id)
#
#         print("Testing UPDATE in %s" % self.__class__)
#         update(request, rule_id)
#
#         print("Testing DELETE in %s" % self.__class__)
#         delete(request, rule_id)
#
#
# class TestplanRuleViewTestCase(TestCase):
#     """
#     Test views/testplan_rule.py CRUD
#     This test requires a valid user "admin" with password "admin".
#     """
#
#     def test_crud(self):
#         """
#         Tests CRUD for testplan model.
#         """
#         from views import testplan, testplan_rule
#         import json
#
#         def create_testplan(request):
#             request.body = json.dumps({"name": "CRUD test for testplan_rule"})
#             response = testplan.post(request)
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("location", response._headers)
#             in_json = json.loads(response.content)
#             self.assertIn("id", in_json)
#             return in_json['id']
#
#         def delete_testplan(request, testplan_id):
#             response = testplan.delete(request, testplan_id)
#             self.assertEqual(response.status_code, 200)
#
#         def create(request, testplan_id):
#             request.body = json.dumps({
#                 'ruleType': 'request',
#                 'enabled': True,
#                 'name': 'test_rule_1',
#                 'filter': {
#                     'httpProtocol': 'HTTP/1.1',
#                     'method': 'GET',
#                     'headers': [
#                         {'key': 'foo'},
#                         {'key': 'fizz', 'value': 'buzz'},
#                     ],
#                 },
#                 'action': {
#                     'type': 'modify',
#                     'method': 'PUT',
#                     'url': 'www.newurl.com/foo/bar',
#                     'setHeaders': [
#                         {
#                             'key': 'zaphod', 'value': 'beeblebrox',
#                         },
#                     ],
#                     'deleteHeaders': [
#                         {
#                             'key': 'foo',
#                         },
#                     ],
#                 }
#             })
#             response = testplan_rule.post(request, testplan_id)
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("location", response._headers)
#             in_json = json.loads(response.content)
#             self.assertIn("id", in_json)
#             return in_json['id']
#
#         def read(request, testplan_id, rule_id):
#             response = testplan_rule.get(request, testplan_id, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         def update(request, testplan_id, rule_id):
#             request.body = json.dumps({
#                 'ruleType': 'request',
#                 'enabled': True,
#                 'name': 'test_rule_4',
#                 'filter': {
#                     'httpProtocol': 'HTTP/1.1',
#                     'method': 'GET',
#                     'headers': [
#                         {'key': 'folk hero'},
#                         {'key': 'instrument', 'value': 'violin'},
#                     ],
#                 },
#                 'action': {
#                     'type': 'newResponse',
#                     'httpProtocol': 'CARRIERFLAMINGO/1.1',
#                     'statusCode': 403,
#                     'statusDescription': 'TOO FEATHERY',
#                     'headers': [
#                         {
#                             'key': 'User-Agent',
#                             'value': 'Broken Looking Glass 1.9'
#                         },
#                     ],
#                     'payload': 'The answer to life, the universe, and everything...is----NO CARRIER.',
#                 }
#
#             })
#             response = testplan_rule.put(request, testplan_id, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         def delete(request, testplan_id, rule_id):
#             response = testplan_rule.delete(request, testplan_id, rule_id)
#             self.assertEqual(response.status_code, 200)
#
#         print("Creating authenticated request for CRUD tests in %s" % self.__class__)
#         request = create_authenticated_request("admin", "admin")
#         request.method = "POST"
#
#         print("Creating temporary testplan for use within %s" % self.__class__)
#         testplan_id = create_testplan(request)
#
#         print("Testing CREATE #1 in %s" % self.__class__)
#         rule1_id = create(request, testplan_id)
#
#         print("Testing CREATE #2 in %s" % self.__class__)
#         rule2_id = create(request, testplan_id)
#
#         print("Testing READ in %s" % self.__class__)
#         read(request, testplan_id, rule1_id)
#
#         print("Testing UPDATE in %s" % self.__class__)
#         update(request, testplan_id, rule1_id)
#
#         print("Testing DELETE #1 in %s" % self.__class__)
#         delete(request, testplan_id, rule1_id)
#
#         print("Testing DELETE #2 in %s" % self.__class__)
#         delete(request, testplan_id, rule2_id)
#
#         print("Removing temporary testplan for use within %s" % self.__class__)
#         delete_testplan(request, testplan_id)
#
#
# class RecordingViewTestCase(TestCase):
#     """
#     Test views/recording.py CRUD
#     This test requires a valid user "admin" with password "admin".
#     """
#
#     def test_crud(self):
#         """
#         Tests CRUD for recording model.
#         """
#         from views import recording
#         import json
#
#         def create(request):
#             request.body = json.dumps({
#                 "name": "CRUD test for recording",
#             })
#             response = recording.post(request)
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("location", response._headers)
#             in_json = json.loads(response.content)
#             self.assertIn("id", in_json)
#             return in_json['id']
#
#         def read(request, recording_id):
#             response = recording.get(request, recording_id)
#             self.assertEqual(response.status_code, 200)
#
#         def update(request, recording_id):
#             request.body = json.dumps({
#                 "name": "CRUD test for recording, updated",
#                 "description": "description...",
#             })
#             response = recording.put(request, recording_id)
#             self.assertEqual(response.status_code, 200)
#
#         def delete(request, recording_id):
#             response = recording.delete(request, recording_id)
#             self.assertEqual(response.status_code, 200)
#
#         print("Creating authenticated request for CRUD tests in %s" % self.__class__)
#         request = create_authenticated_request("admin", "admin")
#         request.method = "POST"
#
#         print("Testing CREATE in %s" % self.__class__)
#         recording_id = create(request)
#
#         print("Testing READ in %s" % self.__class__)
#         read(request, recording_id)
#
#         print("Testing UPDATE in %s" % self.__class__)
#         update(request, recording_id)
#
#         print("Testing DELETE in %s" % self.__class__)
#         delete(request, recording_id)
