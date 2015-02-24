from django.test import TestCase


def create_authenticated_request(username, password):
    """
    Return a request object with a valid X-AUTH-TOKEN
    """
    import requests
    from views import auth
    import json

    request = requests.Request()
    request.method = "POST"

    # Acquire valid token to test with
    request.body = json.dumps(dict(username=username, password=password))
    response = auth.login(request)
    token = response._headers['x-auth-token'][1]
    request.META = {'HTTP_X_AUTH_TOKEN': token}

    # Unset request attributes other than the auth token, then return it
    request.body = ''
    request.method = ''
    return request


class AuthViewTestCase(TestCase):
    """
    Test views/auth.py
    This test requires a valid user "admin" with password "admin".
    """

    def test_login(self):
        """
        Logs in and asserts x-auth-token in response.
        """
        from views import auth
        import json
        import requests

        print("Testing LOGIN in %s" % self.__class__)
        request = requests.Request()
        request.method = "POST"
        request.body = json.dumps(dict(username="admin", password="admin"))
        response = auth.login(request)
        assert "x-auth-token" in response._headers


class SessionViewTestCase(TestCase):
    """
    Test views/session.py CRUD
    This test requires a valid user "admin" with password "admin".
    """

    def test_crud(self):
        """
        Tests CRUD for session model.
        """
        from views import session, testplan
        import json

        def create(request):
            request.body = json.dumps({
                'name': 'CRUD test',
                'description': 'CRUD test',
                })
            response = session.post(request)
            assert response.status_code == 200
            assert "location" in response._headers
            in_json = json.loads(response.content)
            assert "_id" in in_json
            session_id = in_json['_id']
            return session_id

        def read(request, session_id):
            response = session.get(request, session_id)
            assert response.status_code == 200

            response = session.get(create_authenticated_request("test1", "test1"), session_id)
            assert response.status_code == 401

        def update(request, session_id):
            request.body = json.dumps({'name': 'CRUD test updated'})
            response = session.put(request, session_id)
            assert response.status_code == 200

            user1_request = create_authenticated_request("test1", "test1")
            user1_request.body = json.dumps({'name': 'CRUD test updated'})
            response = session.put(user1_request, session_id)
            assert response.status_code == 401

        def delete(request, session_id):
            response = session.delete(create_authenticated_request("test1", "test1"), session_id)
            assert response.status_code == 401

            response = session.delete(request, session_id)
            assert response.status_code == 200

        def linked_crud(request):
            # Create a testplan
            request.body = json.dumps({"name": "crud testplan"})
            response = testplan.post(request)
            assert response.status_code == 200
            testplan_id = json.loads(response.content)['_id']

            # Create a session linked to testplan
            request.body = json.dumps({
                'name': 'crud session',
                'description': 'crud session description',
                'testplan': testplan_id,
            })
            response = session.post(request)
            assert response.status_code == 200
            session_id = json.loads(response.content)['_id']

            # Delete session and testplan
            response = session.delete(request, session_id)
            assert response.status_code == 200
            response = testplan.delete(request, testplan_id)
            assert response.status_code == 200

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request("admin", "admin")
        request.method = "POST"

        print("Testing CREATE in %s" % self.__class__)
        session_id = create(request)

        print("Testing READ in %s" % self.__class__)
        read(request, session_id)

        print("Testing UPDATE in %s" % self.__class__)
        update(request, session_id)

        print("Testing DELETE in %s" % self.__class__)
        delete(request, session_id)

        print("Testing CRUD specific to a linked testplan in %s" % self.__class__)
        linked_crud(request)


class TestplanViewTestCase(TestCase):
    """
    Test views/testplan.py CRUD
    This test requires a valid user "admin" with password "admin".
    """

    def test_crud(self):
        """
        Tests CRUD for testplan model.
        """
        from views import testplan
        import json

        def create(request):
            request.body = json.dumps({"name": "CRUD test"})
            response = testplan.post(request)
            assert response.status_code == 200
            assert "location" in response._headers
            in_json = json.loads(response.content)
            assert "_id" in in_json
            return in_json['_id']

        def read(request, testplan_id):
            response = testplan.get(request, testplan_id)
            assert response.status_code == 200

        def update(request, testplan_id):
            request.body = json.dumps({"name": "CRUD test updated"})
            response = testplan.put(request, testplan_id)
            assert response.status_code == 200

        def delete(request, testplan_id):
            response = testplan.delete(request, testplan_id)
            assert response.status_code == 200

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request("admin", "admin")
        request.method = "POST"

        print("Testing CREATE in %s" % self.__class__)
        testplan_id = create(request)

        print("Testing READ in %s" % self.__class__)
        read(request, testplan_id)

        print("Testing UPDATE in %s" % self.__class__)
        update(request, testplan_id)

        print("Testing DELETE in %s" % self.__class__)
        delete(request, testplan_id)


class UserViewTestCase(TestCase):
    """
    Test views/user.py CRUD
    This test requires a valid user "admin" with password "admin".
    """

    def test_crud(self):
        """
        Tests CRUD for user model.
        """
        from views import user
        import json

        def create(request):
            username = "crudtest"
            request.body = json.dumps({
                "username": username,
                "password": "CRUD test",
                "email": "test@test",
            })
            response = user.post(request)
            assert response.status_code == 200
            assert "location" in response._headers

            response = user.post(create_authenticated_request("test1", "test1"))
            assert response.status_code == 401

            return username

        def read(request, username):
            response = user.get(request, username)
            assert response.status_code == 200

            response = user.get_all_users(request)
            assert response.status_code == 200

            response = user.get_all_users(create_authenticated_request("test1", "test1"))
            assert response.status_code == 401

        def update(request, username):
            request.body = json.dumps({"email": "test1@test1"})
            response = user.put(request, username)
            assert response.status_code == 200

            response = user.put(create_authenticated_request("test1", "test1"), username)
            assert response.status_code == 401

        def delete(request, username):

            response = user.delete(create_authenticated_request("test1", "test1"), username)
            assert response.status_code == 401

            response = user.delete(request, username)
            assert response.status_code == 200

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request("admin", "admin")
        request.method = "POST"

        print("Testing CREATE in %s" % self.__class__)
        username = create(request)

        print("Testing READ in %s" % self.__class__)
        read(request, username)

        print("Testing UPDATE in %s" % self.__class__)
        update(request, username)

        print("Testing DELETE in %s" % self.__class__)
        delete(request, username)


class TrafficViewTestCase(TestCase):
    """
    Test views/traffic.py CRUD
    This test requires a valid user "admin" with password "admin".
    """

    def test_crud(self):
        """
        Tests CRUD for traffic model.
        """
        from views import traffic
        from models import snippet_generator

        def create(request):
            pass

        def read(request):
            response = traffic.get(request)
            assert response.status_code == 200

        def update(request, username):
            pass

        def delete(request, username):
            pass

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request("admin", "admin")
        request.method = "POST"

        print("Generating test traffic in Redis")
        snippet_generator.generate_traffic()

        print("Testing READ in %s" % self.__class__)
        read(request)


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
#         from views import testplan, rule
#         import json
#
#         def create(request):
#             request.body = json.dumps({"name": "CRUD test"})
#
#             # First create a test plan to hold our rules
#             response = testplan.post(request)
#             assert response.status_code == 200
#             assert "location" in response._headers
#             in_json = json.loads(response.content)
#             assert "_id" in in_json
#             testplan_id = in_json['_id']
#
#             # Create rule within the test plan
#             request.body = json.dumps({
#                 "ruleType": "request",
#                 "action": {
#                     "type": "request",
#                     "headers": [['header1-name', 'header1-value'], ['header2-name', 'header2-value']],
#                     "request": {
#                         "http_protocol": "HTTP/2.0",
#                         "method": "UPDATE",
#                         "url": "http://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy",
#                         "payload": "MOSTLY HARMLESS",
#                     }
#                 },
#                 "filter": {
#                     "method": "PUT",
#                     "statusCode": 200,
#                     "url": "http://test.com",
#                     "protocol": "HTTP/1.1",
#                     "headers": [['header1-name', 'header1-value'], ['header2-name', 'header2-value']],
#                 },
#             })
#             response = rule.post(request, testplan_id=testplan_id)
#             assert response.status_code == 200
#             in_json = json.loads(response.content)
#             rule_id = in_json['id']
#
#             return testplan_id, rule_id
#
#         def read(request, rule_id, testplan_id):
#             response = rule.get(request, testplan_id, rule_id)
#             assert response.status_code == 200
#             response_json = json.loads(response.content)
#             assert "ruleType" in response_json
#             assert response_json['ruleType'] == 'request'
#             assert int(response_json['testPlanId'] == testplan_id)
#
#         def update(request, rule_id):
#             request.body = json.dumps({
#                 "ruleType": "response",
#                 "action": {
#                     "type": "response",
#                     "headers": [['new-header1-name', 'new-header1-value'], ['new-header2-name', 'new-header2-value']],
#                     "response": {
#                         "http_protocol": "HTTP/2.0",
#                         "status_code": 503,
#                         "status_description": "Service Unavailable",
#                         "payload": "FISHY",
#                     },
#                     "request": {
#                         "http_protocol": "HTTP/2.0",
#                         "method": "UPDATE",
#                         "url": "http://en.wikipedia.org/wiki/So_Long,_and_Thanks_for_All_the_Fish",
#                         "payload": "LESS FISHY",
#                     }
#                 },
#                 "filter": {
#                     "method": "GET",
#                     "statusCode": 404,
#                     "url": "http://newtest.com",
#                     "protocol": "HTTPS",
#                     "headers": [['new-header1-name', 'new-header1-value'], ['new-header2-name', 'new-header2-value']],
#                 },
#             })
#             response = rule.put(request, rule_id)
#             assert response.status_code == 200
#
#         def delete(request, rule_id):
#             response = rule.delete(request, rule_id)
#             assert response.status_code == 200
#
#         print("Creating authenticated request for CRUD tests in %s" % self.__class__)
#         request = create_authenticated_request("admin", "admin")
#         request.method = "POST"
#
#         print("Testing CREATE in %s" % self.__class__)
#         testplan_id, rule_id = create(request)
#
#         print("Testing READ in %s" % self.__class__)
#         read(request, rule_id, testplan_id)
#
#         print("Testing UPDATE in %s" % self.__class__)
#         update(request, rule_id)
#
#         print("Testing DELETE in %s" % self.__class__)
#         delete(request, rule_id)
