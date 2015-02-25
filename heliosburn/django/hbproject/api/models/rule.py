# Validation model for a 'Rule'


def validate(rule):
    """
    Validate a rule within a dictionary. Returns a validated copy of the `rule` dict, or None if validation fails.

    NOTE: Type conversions are attempted(eg str-to-int), but incompatible data types will still cause a failure.
    """

    try:
        new_rule = {}
        assert 'type' in rule
        assert (rule['type'] == 'request') or (rule['type'] == 'response')

        # Verify filter
        assert 'filter' in rule
        assert type(rule['filter']) is dict
        with rule['filter'] as f:
            if rule['type'] == 'request':  # members specific to 'request' filter
                if 'method' in f:
                    new_rule['filter']['method'] = str(f['method'])
                if 'url' in f:
                    new_rule['filter']['url'] = str(f['url'])
            elif rule['type'] == 'response':  # members specific to 'response' filter
                if 'statusCode' in f:
                    new_rule['statusCode'] = int(f['statusCode'])

            # members in both 'request' or 'response' filters
            if 'httpProtocol' in f:
                new_rule['filter']['httpProtocol'] = str(f['httpProtocol'])
            if ('headers' in f) and (type(f['headers']) is list):
                new_rule['headers'] = f['headers']

        # Verify action
        assert 'action' in rule
        with rule['action'] as a:
            if rule['type'] == 'request':
                if 'newRequest' in a:
                    pass  # TODO: handle newrequest members
            if rule['type'] == 'response':
                pass
            if 'modify' in a:
                pass  # TODO: handle contexts in which modify is given
            if 'newResponse' in a:
                pass  # TODO: handle newresponse members
            if 'drop' in a:
                new_rule['drop'] = bool(a['drop'])
            if 'reset' in a:
                new_rule['reset'] = bool(a['reset'])

        return new_rule
    except (AssertionError, KeyError, ValueError) as e:
        return None