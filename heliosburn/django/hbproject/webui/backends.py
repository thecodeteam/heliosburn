from django.conf import settings
from django.contrib.auth.models import User
import requests
import json


class HeliosAuthBackend(object):
    """
    Authenticate against the API.
    """

    def authenticate(self, username=None, password=None):

        payload = {'username': username, 'password': password}
        url = '%s/auth/login/' % (settings.API_BASE_URL,)
        r = requests.post(url, data=json.dumps(payload))

        if r.status_code == requests.codes.ok:

            token = r.headers.get('x-auth-token')
            if not token:
                return None

            try:
                user = User.objects.get(username=username)
                user.password = token
                user.save()
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password=token)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None