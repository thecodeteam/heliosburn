import re


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