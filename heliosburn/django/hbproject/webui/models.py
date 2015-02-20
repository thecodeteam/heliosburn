import json
import re
from django.conf import settings
import requests
from webui.exceptions import BadRequestException, UnauthorizedException, ServerErrorException, RedirectException, UnexpectedException, LocationHeaderNotFoundException


def validate_response(response):
    if 200 <= response.status_code < 300:
        return True
    return False


def status_code_to_exception(status_code):
    if status_code == 400:
        return BadRequestException()
    if status_code == 401:
        return UnauthorizedException()
    if status_code >= 500:
        return ServerErrorException()
    if 300 <= status_code < 400:
        return RedirectException()
    return UnexpectedException()


def get_resource_id_from_header(resource_name, response):
    location = response.headers.get('location')
    pattern = '.+{}\/(?P<id>\d+)'.format(resource_name)
    p = re.compile(pattern)
    m = p.match(location)
    try:
        resource_id = m.group('id')
        return resource_id
    except:
        return None


class Base(object):

    def __init__(self, auth_token=None):
        self.auth_token = auth_token

    def get_url(self, extra=''):
        return '{base_url}{endpoint}{extra}'.format(base_url=settings.API_BASE_URL,
                                                    endpoint=object.__getattribute__(self, '__endpoint__'),
                                                    extra=extra)


class TestPlan(Base):

    __endpoint__ = '/testplan/'
    __classname__ = 'testplan'

    def __init__(self, data=None, auth_token=None):
        self.auth_token = auth_token
        self.data = data

    def save(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(self.data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        resource_id = get_resource_id_from_header('testplan', response)
        if not resource_id:
            raise LocationHeaderNotFoundException()
        return resource_id