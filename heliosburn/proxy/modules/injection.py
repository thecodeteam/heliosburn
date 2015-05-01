from module import AbstractModule
from twisted.python import log


# Dummy function used to test until engine exists
def process_request(http_metadata, session):

    action = {
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

    return action


# Dummy function used to test until engine exists
def process_response(http_metadata, session):
    action = {
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

    return action


class InjectionAction(object):

    def __init__(self, action_dict, request=None, response=None):
        self.action_dict = action_dict
        self.request = request
        self.response = response

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
        return None


class ResetAction(InjectionAction):
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
        'reset': ResetAction
    }

    def handle_request(self, request):
        action_dict = process_request("", "")
        action_type = action_dict['action']['type']
        action = self.actions[action_type](action_dict=action_dict,
                                           request=request)
        result = action.execute()
        if result:
            return request

    def handle_response(self, response):
        action_dict = process_response("", "")
        action_type = action_dict['action']['type']
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
