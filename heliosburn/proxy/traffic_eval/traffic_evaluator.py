from pymongo import MongoClient


class TrafficEvaluator(object):
    def __init__(self, config):
        """
        Returns a TrafficEvaluator object.

        `config` is a dict() object, the deserialized JSON result of the HTTP GET `/api/config`
        """
        config = config['config']
        client = MongoClient(host=config['mongodb']['host'], port=config['mongodb']['port'])
        return client[config['mongodb']['db']['production']]

    def process_traffic(self, http_metadata, session):
        """
        Matches traffic against the rule associated with a session's testplan.

        If a match occurs, the `action` for that rule is returned.
        If no match occurs, `None` is returned.
        """
        return None