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
                'name': 'test session',
                'description': 'test session',
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
            request.body = json.dumps({'name': 'updated name'})
            response = session.put(request, session_id)
            assert response.status_code == 204

        def delete(request, session_id):
            response = session.delete(request, session_id)
            assert response.status_code == 204

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