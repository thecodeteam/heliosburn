from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from api.models.auth import RequireLogin
from api.decorators import RequireDB
from sqlalchemy.exc import IntegrityError
import json


@csrf_exempt
def rest(request, *pargs):
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
        return rest_function(request, *pargs)
    except TypeError:
        return HttpResponseBadRequest("argument mismatch")


@RequireLogin()
@RequireDB()
def get(request, rule_id, dbsession=None):
    """
    Retrieve rule based on testplan_id and rule_id.
    """
    rule = dbsession.query(db_model.Rule).filter_by(id=rule_id).first()
    if rule is None:
        return HttpResponseNotFound()
    else:
        return JsonResponse({
            'id': rule.id,
            'ruleType': rule.rule_type,
            'testPlanId': rule.testplan_id,
            }, status=200)

@csrf_exempt
@RequireLogin()
@RequireDB()
def get_all_rules(request, testplan_id, dbsession=None):
    """
    Retrieve all rules for a test plan.
    """
    rules = dbsession.query(db_model.Rule).filter_by(testplan_id=int(testplan_id)).all()
    rule_list = list()
    for rule in rules:
        rule_list.append({
            'id': rule.id,
            'ruleType': rule.rule_type,
            'testPlanId': rule.testplan_id,
        })
    return JsonResponse({"rules": rule_list})



@RequireLogin()
@RequireDB()
def post(request, testplan_id, dbsession=None):
    """
    Create new rule for testplan marked by testplan_id.
    """
    try:
        new = json.loads(request.body)
        assert "ruleType" in new
        assert (new['ruleType'] == "response") or (new['ruleType'] == "request")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")

    rule = db_model.Rule(rule_type=new['ruleType'], testplan_id=testplan_id)
    dbsession.add(rule)
    try:
        dbsession.commit()
    except IntegrityError:
        return HttpResponseBadRequest("constraint violated")
    return JsonResponse({"id": rule.id})


@RequireLogin()
@RequireDB()
def put(request, rule_id, dbsession=None):
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
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)



@RequireLogin()
@RequireDB()
def delete(request, rule_id, dbsession=None):
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