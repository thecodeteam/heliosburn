from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import legacy_db_model
from api.models import db_model
from bson import ObjectId
from pymongo.helpers import DuplicateKeyError
from api.models.auth import RequireLogin
from sqlalchemy.exc import IntegrityError
import json


@csrf_exempt
def rest(request, *pargs, **kwargs):
    """
    Calls python function corresponding with HTTP METHOD name.
    Calls with incomplete arguments will return HTTP 400
    """
    if request.method == 'GET':
        rest_function = get
    elif request.method == 'POST':
        rest_function = post
    elif request.method == 'PUT':
        rest_function = put
    elif request.method == 'DELETE':
        rest_function = delete
    else:
        return JsonResponse({"error": "HTTP METHOD UNKNOWN"})

    try:
        return rest_function(request, *pargs, **kwargs)
    except TypeError:
        return HttpResponseBadRequest("argument mismatch")


@RequireLogin()
def get(request, testplan_id, rule_id=None):
    """
    Retrieve rule based on testplan_id and rule_id.
    """
    if rule_id is None:
        return get_all_rules(request, testplan_id)
    dbc = db_model.connect()
    rule = dbc.rule.find_one({"_id": ObjectId(rule_id)}, {"_id": 0})
    if rule is None:
        return HttpResponseNotFound()
    else:
        rule['id'] = rule_id  # Replace ObjectId with str version
        return JsonResponse(rule, status=200)


def get_all_rules(request, testplan_id):
    """
    Retrieve all rules for a test plan.
    """
    dbc = db_model.connect()
    rules = [r for r in dbc.rule.find()]
    for rule in rules:
        rule['id'] = str(rule.pop('_id'))
    return JsonResponse({"rules": rules})


@RequireLogin()
def post(request, testplan_id, rule_id=None, dbsession=None):
    """
    Create new rule for testplan marked by testplan_id.
    """
    if request.method != 'POST':
        r = HttpResponse('Invalid method. Only POST method accepted.', status=405)
        r['Allow'] = 'POST'
        return r
    try:
        new = json.loads(request.body)
        assert "ruleType" in new
        assert (new['ruleType'] == "response") or (new['ruleType'] == "request")
        if "action" in new:
            assert "type" in new['action']
            assert ("response" in new['action']) or ("request" in new['action'])
            assert "headers" in new['action']
        if "filter" in new:
            assert "method" in new['filter']
            assert "statusCode" in new['filter']
            assert "url" in new['filter']
            assert "protocol" in new['filter']
            assert "headers" in new['filter']
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")

    dbc = db_model.connect()
    rule = new  # TODO: replace this with validation steps

    rule_id = str(dbc.rule.save(rule))
    r = JsonResponse({"id": rule_id})
    r['location'] = "/api/testplan/%s/rule/%s" % (testplan_id, rule_id)
    return r

@RequireLogin()
def put(request, rule_id, testplan_id=None, dbsession=None):
    """
    Update existing rule based on rule_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    rule = dbsession.query(legacy_db_model.Rule).filter_by(id=rule_id).first()
    if rule is None:
        return HttpResponseNotFound()
    else:
        if "ruleType" in in_json:
            if (in_json['ruleType'] == 'request') or (in_json['ruleType'] == 'response'):
                rule.rule_type = in_json['ruleType']
            else:
                return HttpResponseBadRequest("argument mismatch")
        if "testPlanId" in in_json:
            rule.testplan_id = int(in_json['testplan_id'])

        # Handle actions
        if "action" in in_json:
            if "type" in in_json['action']:
                rule.action.type = in_json['action']['type']
            if "headers" in in_json['action']:
                headers = list()
                for header_name, header_value in in_json['action']['headers']:
                    headers.append(legacy_db_model.ActionHeaders(key=header_name, value=header_value))
                map(dbsession.delete, rule.action.headers)
                rule.action.headers = headers

            # Action response
            if (rule.action.type == "response") and ('response' in in_json['action']):
                rule.action.response = legacy_db_model.ActionResponse(
                    id=rule.action.id,
                    http_protocol=in_json['action']['response']['http_protocol'],
                    status_code=in_json['action']['response']['status_code'],
                    status_description=in_json['action']['response']['status_description'],
                    payload=in_json['action']['response']['payload']
                )

            # Action request
            if (rule.action.type == "request") and ('request' in in_json['action']):
                rule.action.request = legacy_db_model.ActionRequest(
                    id=rule.action.id,
                    http_protocol=in_json['action']['request']['http_protocol'],
                    method=in_json['action']['request']['method'],
                    url=in_json['action']['request']['url'],
                    payload=in_json['action']['request']['payload']
                )


        # Handle filters
        if "filter" in in_json:
            if "method" in in_json['filter']:
                rule.filter.method = in_json['filter']['method']
            if "statusCode" in in_json['filter']:
                rule.filter.status_code = in_json['filter']['statusCode']
            if "url" in in_json['filter']:
                rule.filter.url = in_json['filter']['url']
            if "protocol" in in_json['filter']:
                rule.filter.protocol = in_json['filter']['protocol']
            if "headers" in in_json['filter']:
                headers = list()
                for header_name, header_value in in_json['filter']['headers']:
                    headers.append(legacy_db_model.FilterHeaders(key=header_name, value=header_value))
                map(dbsession.delete, rule.filter.headers)
                rule.filter.headers = headers
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)



@RequireLogin()
def delete(request, rule_id, testplan_id=None):
    """
    Delete rule based on rule_id.
    """
    dbc = db_model.connect()
    rule = dbc.rule.find_one({'_id': ObjectId(rule_id)})
    if rule is None:
        return HttpResponseNotFound()
    else:
        dbc.rule.remove(rule)
        return HttpResponse(status=200)