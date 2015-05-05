from pymongo import MongoClient
from bson import ObjectId


class TrafficEvaluator(object):
    def __init__(self, config):
        """
        Returns a TrafficEvaluator object.

        `config` is a dict() object, the deserialized JSON result of the HTTP GET `/api/config`
        """
        config = config['config']
        client = MongoClient(host=config['mongodb']['host'], port=config['mongodb']['port'])
        self.dbc = client[config['mongodb']['db']['production']]
        return None

    def _eval_rules(self, http_metadata, rules):
        """
        Test `http_metadata` against individual rules, returning the first action of a matching rule.

        If no rules match `http_metadata`, returns `None`.
        """
        if "response" in http_metadata:
            subject = http_metadata['response']
            type = 'response'
        else:
            subject = http_metadata['request']
            type = 'request'

        # Reduce rules to ones that match relevant ruleType
        relevant_rules = []
        for rule in rules:
            if type == rule['ruleType']:
                relevant_rules.append(rule)

        # Test rule components against subject
        for rule in relevant_rules:
            # Test rule.enabled
            if self._eval_rule_enabled(rule) is False:
                return None

            # Test rule.filter components
            if self._eval_rule_filter(rule['filter'], subject) is True:
                return rule['action']

    def _eval_rule_enabled(self, rule):
        """
        Test if a rule has the `enabled` key, and if it is `False`. Returns `True` unless the key exists and is `False`.
        """
        if 'enabled' not in rule:
            return True
        elif ('enabled' in rule) and (rule['enabled'] is True):
            return True
        elif ('enabled' in rule) and (rule['enabled'] is False):
            return False

    def _eval_rule_filter(self, filter, http_metadata):
        """
        Test `filter` components against `http_metadata`. Return `True` if any match, else `False`.
        """
        import re

        # Separate filter headers from filter if they exist
        if 'headers' in filter:
            filter_headers = filter.pop('headers')
        else:
            filter_headers = []

        # Test everything EXCEPT headers, which are evaluated later
        for filter_key in filter.keys():
            if (filter_key in http_metadata) and (re.match(filter[filter_key], http_metadata[filter_key]) is not None):
                return True

        if 'headers' not in http_metadata:  # No headers? This shouldn't happen, but if it does, return False.
            return False

        # Test filter headers against http_metadata headers
        for filter_header in filter_headers:

            # Match header filter that only specifies a key, but not a value
            if ('key' in filter_header) and ('value' not in filter_header):
                for header in http_metadata['headers']:
                    if re.match(filter_header['key'], header[0]) is not None:
                        return True
            # Match header filter that specifies a key and a value, keys must be a 100% string match to compare values
            if ('key' in filter_header) and ('value' in filter_header):
                for header in http_metadata['headers']:
                    if filter_header['key'] == header[0] and (re.match(filter_header['value'], header[1]) is not None):
                        return True

        return False

    def _get_rules(self, session_id):
        """
        Return the rule(s) associated with a session->testplan, or `None` if they do not exist.

        Several conditions could cause rule(s) to not exist for a session, such as:
            - Session has no testplan associated with it
            - Session has a testplan indicated, but the testplan does not exist
            - The testplan contains no rules
        """
        session = self.dbc.session.find_one({"_id": ObjectId(session_id)})
        if session is None:  # Session does not exist
            return None
        if 'testplan' not in session:  # Session exists, but has no testplan
            return None
        else:
            testplan_id = session['testplan']

        testplan = self.dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
        if testplan is None:  # testplan's ID is indicated in session, but not does exited in testplan collection
            return None
        elif 'rules' not in testplan:  # Testplan exists, but contains no rules
            return None
        else:  # Return the rules contained within the testplan
            return testplan['rules']

    def get_action(self, http_metadata, session_id):
        """
        Matches traffic against the rule associated with a session's testplan.

        If a match occurs, the `action` for that rule is returned.
        If no match occurs, `None` is returned.
        """
        rules = self._get_rules(session_id)
        if rules is None:
            return None
        else:
            action = self._eval_rules(http_metadata, rules)
            return action
