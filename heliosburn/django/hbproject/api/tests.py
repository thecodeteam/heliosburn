from django.test import TestCase


def create_authenticated_request():
    """
    Return a request object with a valid X-AUTH-TOKEN
    """
    import requests
    from views import auth
    import json

    request = requests.Request()
    request.method = "POST"

    # Acquire valid token to test with
    request.body = json.dumps(dict(username="admin", password="admin"))
    response = auth.login(request)
    token = response._headers['x-auth-token']
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
        from views import session
        import json

        def create(request):
            request.body = json.dumps({
                'name': 'CRUD test',
                'description': 'CRUD test',
                })
            response = session.post(request)
            assert response.status_code == 200
            in_json = json.loads(response.content)
            assert "id" in in_json
            session_id = in_json['id']
            return session_id

        def read(request, session_id):
            request.body = ''
            response = session.get(request, session_id)
            assert response.status_code == 200

        def update(request, session_id):
            request.body = json.dumps({'name': 'CRUD test updated'})
            response = session.put(request, session_id)
            assert response.status_code == 200

        def delete(request, session_id):
            response = session.delete(request, session_id)
            assert response.status_code == 200

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request()
        request.method = "POST"

        print("Testing CREATE in %s" % self.__class__)
        session_id = create(request)

        print("Testing READ in %s" % self.__class__)
        read(request, session_id)

        print("Testing UPDATE in %s" % self.__class__)
        update(request, session_id)

        print("Testing DELETE in %s" % self.__class__)
        delete(request, session_id)


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
            in_json = json.loads(response.content)
            assert "id" in in_json
            return in_json['id']

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
        request = create_authenticated_request()
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
            return username

        def read(request, username):
            response = user.get(request, username)
            assert response.status_code == 200

        def update(request, username):
            request.body = json.dumps({"email": "test1@test1"})
            response = user.put(request, username)
            assert response.status_code == 200

        def delete(request, username):
            response = user.delete(request, username)
            assert response.status_code == 200

        print("Creating authenticated request for CRUD tests in %s" % self.__class__)
        request = create_authenticated_request()
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
        request = create_authenticated_request()
        request.method = "POST"

        print("Generating test traffic in Redis")
        snippet_generator.generate_traffic()

        print("Testing READ in %s" % self.__class__)
        read(request)