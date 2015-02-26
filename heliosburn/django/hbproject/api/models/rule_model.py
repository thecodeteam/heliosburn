# Validation model for a 'Rule'


def validate(rule):
    """
    Validate a rule within a dictionary. Returns a validated copy of the `rule` dict, or None if validation fails.

    NOTE: Type conversions are attempted(eg str-to-int), but incompatible data types will still cause a failure.
    """

    try:
        new_rule = {}
        assert 'ruleType' in rule
        assert rule['ruleType'] in ('request', 'response')
        new_rule['ruleType'] = rule['ruleType']

        # Validate filter
        assert 'filter' in rule
        assert type(rule['filter']) is dict
        new_rule['filter'] = {}

        if rule['ruleType'] == 'request':  # members specific to 'request' filter
            if 'method' in rule['filter']:
                new_rule['filter']['method'] = str(rule['filter']['method'])
            if 'url' in rule['filter']:
                new_rule['filter']['url'] = str(rule['filter']['url'])
        elif rule['ruleType'] == 'response':  # members specific to 'response' filter
            if 'statusCode' in rule['filter']:
                new_rule['statusCode'] = int(rule['filter']['statusCode'])

        # members in both 'request' or 'response' filters
        if 'httpProtocol' in rule['filter']:
            new_rule['filter']['httpProtocol'] = str(rule['filter']['httpProtocol'])
        if ('headers' in rule['filter']) and (type(rule['filter']['headers']) is list):
            new_rule['filter']['headers'] = rule['filter']['headers']

        # Validate action
        assert 'action' in rule
        assert 'type' in rule['action']
        assert rule['action']['type'] in ('modify', 'newResponse', 'newRequest', 'drop', 'reset')
        new_rule['action'] = {'type': rule['action']['type']}

        if rule['action']['type'] == 'modify':
            if 'method' in rule['action']:
                new_rule['action']['method'] = str(rule['action']['method'])
            if 'url' in rule['action']:
                new_rule['action']['url'] = str(rule['action']['url'])
            if 'statusCode' in rule['action']:
                new_rule['action']['statusCode'] = int(rule['action']['statusCode'])
            if 'statusDescription' in rule['action']:
                new_rule['action']['statusDescription'] = str(rule['action']['statusDescription'])
            if 'httpProtocol' in rule['action']:
                new_rule['action']['httpProtocol'] = str(rule['action']['httpProtocol'])
            if ('setHeaders' in rule['action']) and (type(rule['action']['setHeaders']) is list):
                new_rule['action']['setHeaders'] = rule['action']['setHeaders']
            if ('deleteHeaders' in rule['action']) and (type(rule['action']['deleteHeaders']) is list):
                new_rule['action']['deleteHeaders'] = rule['action']['deleteHeaders']
        elif rule['action']['type'] == 'newResponse':
            if 'httpProtocol' in rule['action']:
                new_rule['action']['httpProtocol'] = str(rule['action']['httpProtocol'])
            if 'statusCode' in rule['action']:
                new_rule['action']['statusCode'] = int(rule['action']['statusCode'])
            else:  # Assume that an omitted statusCode should be rewritten as 200 OK
                new_rule['action']['statusCode'] = 200
            if 'statusDescription' in rule['action']:
                new_rule['action']['statusDescrption'] = str(rule['action']['statusDescription'])
            if ('headers' in rule['action']) and (type(rule['action']['headers']) is list):
                new_rule['action']['headers'] = rule['action']['headers']
            if 'payload' in rule['action']:  # payload is NOT typecasted to str, to allow non-str(eg binary) payloads
                new_rule['action']['payload'] = rule['action']['payload']
        elif rule['action']['type'] == 'newRequest':
            if 'httpProtocol' in rule['action']:
                new_rule['action']['httpProtocol'] = str(rule['action']['httpProtocol'])
            if 'method' in rule['action']:
                new_rule['action']['method'] = str(rule['action']['method'])
            if 'url' in rule['action']:
                new_rule['action']['url'] = str(rule['action']['url'])
            if ('headers' in rule['action']) and (type(rule['action']['headers']) is list):
                new_rule['action']['headers'] = rule['action']['headers']
            if 'payload' in rule['action']:  # payload is NOT typecasted to str, to allow non-str(eg binary) payloads
                new_rule['action']['payload'] = rule['action']['payload']

        return new_rule
    except (KeyError, TypeError, AssertionError):
        return None

test_rule = {
    'ruleType': 'request',
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
}
