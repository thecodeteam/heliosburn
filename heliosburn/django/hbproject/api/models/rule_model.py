# Validation model for a 'Rule'

from bson import ObjectId


def validate(rule):
    """
    Validate a rule within a dictionary. Returns a validated copy of the `rule` dict, or None if validation fails.

    NOTE: Type conversions are attempted(eg str-to-int), but incompatible data types will still cause a failure.
    """
    try:
        new_rule = {}
        if 'createdAt' in rule:
            new_rule['createdAt'] = rule['createdAt']
        if 'updatedAt' in rule:
            new_rule['updatedAt'] = rule['updatedAt']
        if 'id' in rule:
            new_rule['id'] = rule['id']
        else:
            new_rule['id'] = str(ObjectId())
            
        # String constants for key names
        c_name = "name"
        c_description = "description"
        c_ruletype = "ruleType"
        c_filter = "filter"
        c_action = "action"
        c_type = "type"
        c_enabled = "enabled"

        assert c_name in rule
        new_rule[c_name] = rule[c_name]

        if c_enabled in rule:
            try:
                new_rule[c_enabled] = bool(rule[c_enabled])
            except TypeError:
                new_rule[c_enabled] = True
        else:
            new_rule[c_enabled] = True

        if c_description in rule:
            new_rule[c_description] = rule[c_description]

        assert c_ruletype in rule
        assert rule[c_ruletype] in ('request', 'response')
        new_rule[c_ruletype] = rule[c_ruletype]

        # Validate filter
        if c_filter in rule:
            assert c_filter in rule
            assert type(rule[c_filter]) is dict
            new_rule[c_filter] = {}

            # Always get members specific to 'request' filter
            if 'httpProtocol' in rule[c_filter]:
                new_rule[c_filter]['httpProtocol'] = str(rule[c_filter]['httpProtocol'])
            if 'method' in rule[c_filter]:
                new_rule[c_filter]['method'] = str(rule[c_filter]['method'])
            if 'url' in rule[c_filter]:
                new_rule[c_filter]['url'] = str(rule[c_filter]['url'])
            if ('requestHeaders' in rule[c_filter]) and (type(rule[c_filter]['requestHeaders']) is list):
                new_rule[c_filter]['requestHeaders'] = rule[c_filter]['requestHeaders']

            if rule[c_ruletype] == 'response':  # members specific to 'response' filter
                if 'statusCode' in rule[c_filter]:
                    try:
                        new_rule['statusCode'] = int(rule[c_filter]['statusCode'])
                    except TypeError:
                        pass
                if ('responseHeaders' in rule[c_filter]) and (type(rule[c_filter]['responseHeaders']) is list):
                    new_rule[c_filter]['responseHeaders'] = rule[c_filter]['responseHeaders']

        # Validate action
        if c_action in rule:
            assert c_type in rule[c_action]
            assert rule[c_action][c_type] in ('modify', 'newResponse', 'newRequest', 'drop', 'reset')
            new_rule[c_action] = {c_type: rule[c_action][c_type]}

            if rule[c_action][c_type] == 'modify':
                if 'method' in rule[c_action]:
                    new_rule[c_action]['method'] = str(rule[c_action]['method'])
                if 'url' in rule[c_action]:
                    new_rule[c_action]['url'] = str(rule[c_action]['url'])
                if 'statusCode' in rule[c_action]:
                    new_rule[c_action]['statusCode'] = int(rule[c_action]['statusCode'])
                if 'statusDescription' in rule[c_action]:
                    new_rule[c_action]['statusDescription'] = str(rule[c_action]['statusDescription'])
                if 'httpProtocol' in rule[c_action]:
                    new_rule[c_action]['httpProtocol'] = str(rule[c_action]['httpProtocol'])
                if ('setHeaders' in rule[c_action]) and (type(rule[c_action]['setHeaders']) is list):
                    new_rule[c_action]['setHeaders'] = rule[c_action]['setHeaders']
                if ('deleteHeaders' in rule[c_action]) and (type(rule[c_action]['deleteHeaders']) is list):
                    new_rule[c_action]['deleteHeaders'] = rule[c_action]['deleteHeaders']
            elif rule[c_action][c_type] == 'newResponse':
                if 'httpProtocol' in rule[c_action]:
                    new_rule[c_action]['httpProtocol'] = str(rule[c_action]['httpProtocol'])
                if 'statusCode' in rule[c_action]:
                    new_rule[c_action]['statusCode'] = int(rule[c_action]['statusCode'])
                else:  # Assume that an omitted statusCode should be rewritten as 200 OK
                    new_rule[c_action]['statusCode'] = 200
                if 'statusDescription' in rule[c_action]:
                    new_rule[c_action]['statusDescription'] = str(rule[c_action]['statusDescription'])
                if ('headers' in rule[c_action]) and (type(rule[c_action]['headers']) is list):
                    new_rule[c_action]['headers'] = rule[c_action]['headers']
                if 'payload' in rule[c_action]:  # payload is NOT typecasted to str, to allow non-str(eg binary) payloads
                    new_rule[c_action]['payload'] = rule[c_action]['payload']
            elif rule[c_action][c_type] == 'newRequest':
                if 'httpProtocol' in rule[c_action]:
                    new_rule[c_action]['httpProtocol'] = str(rule[c_action]['httpProtocol'])
                if 'method' in rule[c_action]:
                    new_rule[c_action]['method'] = str(rule[c_action]['method'])
                if 'url' in rule[c_action]:
                    new_rule[c_action]['url'] = str(rule[c_action]['url'])
                if ('headers' in rule[c_action]) and (type(rule[c_action]['headers']) is list):
                    new_rule[c_action]['headers'] = rule[c_action]['headers']
                if 'payload' in rule[c_action]:  # payload is NOT typecasted to str, to allow non-str(eg binary) payloads
                    new_rule[c_action]['payload'] = rule[c_action]['payload']

        return new_rule
    except (KeyError, TypeError, AssertionError):
        return None

test_rule = {
    "ruleType": 'request',
    "filter": {
        'httpProtocol': 'HTTP/1.1',
        'method': 'GET',
        'headers': [
            {'key': 'foo'},
            {'key': 'fizz', 'value': 'buzz'},
        ],
    },
    "action": {
        "type": 'modify',
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