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
        request = requests.Request()
        request.method = "POST"
        request.body = json.dumps(dict(username="admin", password="admin"))
        response = auth.login(request)
        assert "x-auth-token" in response._headers


class SessionViewTestCase(TestCase):
    """
    Test views/session.py
    This test requires a valid user "admin" with password "admin".
    """

    def test_crud(self):
        """
        Tests CRUD for session model.
        """
        from views import session
        import json

        # Create a new session
        request = create_authenticated_request()
        request.method = "POST"
        request.body = json.dumps({
            'name': 'test session',
            'description': 'test session',
            })
        response = session.post(request)
        assert response.status_code == 200
        in_json = json.loads(response.content)
        assert "id" in in_json
        session_id = in_json['id']

        # Update session
        request.body = json.dumps({'name': 'updated name'})
        response = session.put(request, session_id)
        assert response.status_code == 204


        # Retrieve session
        request.body = ''
        response = session.get(request, session_id)
        assert response.status_code == 200

        # Delete session
        response = session.delete(request, session_id)
        assert response.status_code == 204