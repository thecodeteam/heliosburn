from module import AbstractModule
from twisted.python import log
from traffic_eval.traffic_evaluator import TrafficEvaluator


# Dummy function used to test until engine exists
drop_test = {
    "action": {
        "type": "drop",
        "payload": "Intercepted by HeliosBurn"
    }}

reset_test = {
    "action": {
        "type": "reset",
        "payload": "Intercepted by HeliosBurn"
    }}

null_test = None

new_request_test = {
    "action": {
        "type": "newRequest",
        "httpProtocol": "HTTP/1.1",
        "statusCode": 400,
        "statusDescription": "Bad Request",
        "headers": [
            {
                "key": "E-Tag",
                "value": "9384253245"
            },
            {
                "key": "Server",
                "value": "HeliosBurn"
            }
        ],
        "payload": "Intercepted by HeliosBurn"
    }}

new_response_test = {
    "action": {
        "type": "newResponse",
        "httpProtocol": "HTTP/1.1",
        "statusCode": 400,
        "statusDescription": "Bad Request",
        "headers": [
            {
                "key": "E-Tag",
                "value": "9384253245"
            },
            {
                "key": "Server",
                "value": "HeliosBurn"
            }
        ],
        "payload": "Intercepted by HeliosBurn"
    }}

config = {
    "config": {
        "redis": {
            "db": 0,
            "port": 6379,
            "host": "localhost"
        },
        "mongodb": {
            "host": "localhost",
            "db": {
                "production": "heliosburn",
                "test": "heliosburng_test"
            },
            "port": 27017
        }
    }
}


def process_request(http_metadata, session):
    injection_engine = TrafficEvaluator(config)
#    injection_engine.get_action("", "")
    action = null_test

    return action


# Dummy function used to test until engine exists
def process_response(http_metadata, session):
    injection_engine = TrafficEvaluator(config)
#    injection_engine.get_action("", "")

    action = drop_test

    return action


class InjectionAction(object):

    def __init__(self, action_dict, request=None, response=None):
        self.action_dict = action_dict
        self.request = request
        self.response = response
        self.injection_engine = TrafficEvaluator(config)

    def execute(self):
        pass


class ModifyAction(InjectionAction):
    def execute(self):
        if self.request:
            return self.request
        else:
            return self.response


class NewResponseAction(InjectionAction):
    def execute(self):
        return self.response


class NewRequestAction(InjectionAction):
    def execute(self):
        return self.request


class DropAction(InjectionAction):
    def execute(self):
        if self.request:
            self.request.drop_connection = True
            return self.request
        else:
            self.response.drop_connection = True
            return self.response


class ResetAction(InjectionAction):
    def execute(self):
        if self.request:
            self.request.reset_connection = True
            return self.request
        else:
            self.response.reset_connection = True
            return self.response


class NullAction(InjectionAction):
    def execute(self):
        if self.request:
            return self.request
        else:
            return self.response


class Injection(AbstractModule):
    actions = {
        'modify': ModifyAction,
        'newResponse': NewResponseAction,
        'newRequest': NewRequestAction,
        'drop': DropAction,
        'reset': ResetAction,
        'null': NullAction
    }

    def handle_request(self, request):
        action_dict = process_request("", "")
        if action_dict:
            action_type = action_dict['action']['type']
        else:
            action_type = 'null'

        action = self.actions[action_type](action_dict=action_dict,
                                           request=request)
        result = action.execute()
        if result:
            return request

    def handle_response(self, response):
        action_dict = process_response("", "")
        if action_dict:
            action_type = action_dict['action']['type']
        else:
            action_type = 'null'

        action = self.actions[action_type](action_dict=action_dict,
                                           response=response)
        result = action.execute()
        if result:
            return response

    def reset(self):
        pass

    def reload(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

injection = Injection()
