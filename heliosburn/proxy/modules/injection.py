import datetime
from module import AbstractModule
from twisted.python import log
from traffic_eval.traffic_evaluator import TrafficEvaluator
from module_decorators import SkipHandler


class InjectionAction(object):

    def __init__(self, action_dict, request=None, response=None):
        self.action_dict = action_dict
        self.request = request
        self.response = response

        self.element_map = {
            "httpProtocol": "clientproto",
            "method": "method",
            "url": "uri",
            "statusCode": "code",
            "payload": "content",
            "statusDescription": "code_message"
        }

    def execute(self):
        pass

    def _add_headers(self, obj, headers):
        for header in headers:
            if obj.responseHeaders:
                obj.responseHeaders.addRawHeader(
                    header['key'], header['value']
                )
            if obj.requestHeaders:
                obj.requestHeaders.addRawHeader(
                    header['key'], header['value']
                )

    def _delete_headers(self, obj, headers):
        for header in headers:
            if obj.responseHeaders:
                obj.responseHeaders.removeHeader(header['key'])
            if obj.requestHeaders:
                obj.requestHeaders.removeHeader(header['key'])

    def _modify(self, obj):
        action = self.action_dict['action']
        for element in self.element_map:
            if element in action:
                setattr(obj, self.element_map[element], action[element])

        if 'headers' in action:
            self._delete_headers(obj, obj.getAllRawHeaders())
            self._add_headers(obj, action['header'])

        if 'setHeaders' in action:
            self._add_headers(obj, action['setHeaders'])

        if 'deleteHeaders' in action:
            self._delete_headers(obj, action['deleteHeaders'])


class ModifyAction(InjectionAction):

    def execute(self):
        if self.request:
            self._modify(self.request)
            log.msg("request after modify: " + str(self.request))
            return self.request
        else:
            self._modify(self.response)
            log.msg("response after modify: " + str(self.response))
            return self.response


class NewResponseAction(InjectionAction):
    def execute(self):
        self._modify(self.response)
        return self.response


class NewRequestAction(InjectionAction):
    def execute(self):
        self._modify(self.request)
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

    def __init__(self):
        AbstractModule.__init__(self)
        self.stats['injection'] = {}

    def configure(self, **configs):
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_db = configs['redis_db']
        self.mongo_host = configs['mongo_host']
        self.mongo_port = configs['mongo_port']
        self.mongo_db = configs['mongo_db']

    def _get_config(self):
        config = {
            "config": {
                "redis": {
                    "db": self.redis_db,
                    "port": self.redis_port,
                    "host": self.redis_host
                },
                "mongodb": {
                    "host": self.mongo_host,
                    "db": {
                        "production": self.mongo_db,
                        "test": "heliosburn_test"
                    },
                    "port": self.mongo_port
                }
            }
        }

        return config

    def _process_request(self, http_metadata, session):
        log.msg("calling traffic evaluator with:\n" +
                "http_metadata: " + str(http_metadata) + "\n"
                "      session: " + str(session))
        action = self.injection_engine.get_action(http_metadata, session)

        return action

    def _process_response(self, http_metadata, session):
        log.msg("calling traffic evaluator with:\n" +
                "http_metadata: " + str(http_metadata) + "\n"
                "      session: " + str(session))
        action = self.injection_engine.get_action(http_metadata, session)

        return action

    @SkipHandler
    def handle_request(self, request):
        request_headers = [[k, v] for (k, v)
                           in request.requestHeaders.getAllRawHeaders()]
        http_metadata = {
            "request": {
                "url": request.uri,
                "httpProtocol": request.clientproto,
                "method": request.method,
                "headers": request_headers
            }
        }

        action_dict = self._process_request(http_metadata, self.session_id)

        if action_dict:
            action_type = action_dict['action']['type']
            action = self.actions[action_type](action_dict=action_dict,
                                               request=request)
            request = action.execute()
            self.stats['injection'][action_type] += 1
        else:
            action_type = 'null'

        log.msg("Injection request: " + str(request))

        return request

    @SkipHandler
    def handle_response(self, response):
        response_headers = [[k, v] for (k, v)
                            in response.responseHeaders.getAllRawHeaders()]

        request_headers = [[k, v] for (k, v)
                           in response.requestHeaders.getAllRawHeaders()]

        http_metadata = {
            "request": {
                "url": response.uri,
                "httpProtocol": response.clientproto,
                "method": response.method,
                "headers": request_headers
            },
            "response": {
                "url": response.uri,
                "httpProtocol": response.clientproto,
                "stausCode": response.code,
                "stausDescription": response.code_message,
                "headers": response_headers
            }
        }

        action_dict = self._process_response(http_metadata, self.session_id)
        if action_dict:
            action_type = action_dict['action']['type']
        else:
            action_type = 'null'

        action = self.actions[action_type](action_dict=action_dict,
                                           response=response)
        response = action.execute()
        log.msg("Injection response: " + str(response))

        return response

    def start(self, **params):
        self.injection_engine = TrafficEvaluator(self._get_config())
        self.session_id = params['session_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        log.msg("Injection module started at: " + self.status)

    def stop(self, **params):
        self.injection_engine = None
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        log.msg("Injection module stopped at: " + self.status)

injection = Injection()
