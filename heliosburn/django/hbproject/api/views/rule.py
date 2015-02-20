from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from api.models.auth import RequireLogin
from api.decorators import RequireDB
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
@RequireDB()
def get(request, testplan_id, rule_id=None, dbsession=None):
    """
    Retrieve rule based on testplan_id and rule_id.
    """
    if rule_id is None:
        return get_all_rules(request, testplan_id, dbsession)
    rule = dbsession.query(db_model.Rule).filter_by(id=rule_id).first()
    if rule is None:
        return HttpResponseNotFound()
    else:
        if rule.filter is not None:
            cur_filter = {
                'id': rule.filter.id,
                'method': rule.filter.method,
                'status_code': rule.filter.status_code,
                'url': rule.filter.url,
                'protocol': rule.filter.protocol,
                'ruleId': rule.filter.rule_id,
                'filterHeaders': [],
            }
        else:
            cur_filter = None

        if rule.action is not None:
            cur_action = {
                'id': rule.action.id,
                'type': rule.action.type,
                'ruleId': rule.action.rule_id,
            }
        else:
            cur_action = None

        return JsonResponse({
            'id': rule.id,
            'ruleType': rule.rule_type,
            'testPlanId': rule.testplan_id,
            'filter': cur_filter,
            'action': cur_action,
            }, status=200)


def get_all_rules(request, testplan_id, dbsession=None):
    """
    Retrieve all rules for a test plan.
    """
    rules = dbsession.query(db_model.Rule).filter_by(testplan_id=int(testplan_id)).all()
    rule_list = list()
    for rule in rules:
        if rule.filter is not None:
            cur_filter = {
                'id': rule.filter.id,
                'method': rule.filter.method,
                'status': rule.filter.status,
                'url': rule.filter.url,
                'protocol': rule.filter.protocol,
                'ruleId': rule.filter.rule_id,
            }
        else:
            cur_filter = None

        if rule.action is not None:
            cur_action = {
                'id': rule.action.id,
                'type': rule.action.type,
                'rule_id': rule.action.rule_id,
            }
        else:
            cur_action = None
        rule_list.append({
            'id': rule.id,
            'ruleType': rule.rule_type,
            'testPlanId': rule.testplan_id,
            'filter': cur_filter,
            'action': cur_action,
        })
    return JsonResponse({"rules": rule_list})



@RequireLogin()
@RequireDB()
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

    rule = db_model.Rule(rule_type=new['ruleType'], testplan_id=testplan_id)
    if 'action' in new:
        action = db_model.Action(type=new['action']['type'])
        rule.action = action
    if 'filter' in new:
        filter = db_model.Filter(method=new['filter']['method'], status_code=new['filter']['statusCode'],
                                 url=new['filter']['url'], protocol=new['filter']['protocol'])
        headers = list()
        for header_name, header_value in new['filter']['headers']:
            headers.append(db_model.FilterHeaders(key=header_name, value=header_value))
        filter.headers = headers
        rule.filter = filter
    dbsession.add(rule)
    try:
        dbsession.commit()
    except IntegrityError:
        return HttpResponseBadRequest("constraint violated")
    r = JsonResponse({"id": rule.id})
    r['location'] = "/api/testplan/%d/rule/%d" % (testplan_id, rule.id)
    return r


@RequireLogin()
@RequireDB()
def put(request, rule_id, testplan_id=None, dbsession=None):
    """
    Update existing rule based on rule_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    rule = dbsession.query(db_model.Rule).filter_by(id=rule_id).first()
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
        if "action" in in_json:
            if "type" in in_json['action']:
                rule.action.type = in_json['action']['type']
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
                    headers.append(db_model.FilterHeaders(key=header_name, value=header_value))
                map(dbsession.delete, rule.filter.headers)
                rule.filter.headers = headers
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)



@RequireLogin()
@RequireDB()
def delete(request, rule_id, testplan_id=None, dbsession=None):
    """
    Delete rule based on rule_id.
    """
    rule = dbsession.query(db_model.Rule).filter_by(id=rule_id).first()
    if rule is None:
        return HttpResponseNotFound()
    else:
        dbsession.delete(rule)
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)