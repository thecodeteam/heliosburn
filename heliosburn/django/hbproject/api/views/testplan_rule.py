from bson import ObjectId
import json

from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import db_model
from api.models.auth import RequireLogin
from api.models import rule_model
from api.models.redis_wrapper import logger


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
def get(request, testplan_id, rule_id):
    """
    Retrieve rule within testplan based on the testplan_id and rule_id.
    """
    dbc = db_model.connect()
    try:
        testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)}, {'_id': 0})
    except InvalidId:
        return HttpResponseNotFound()
    if testplan is None:
        return HttpResponseNotFound()

    rule = filter(lambda r: r['id'] == rule_id, testplan['rules'])
    if len(rule) == 0:
        return HttpResponseBadRequest("rule not found within test plan")
    else:
        return JsonResponse(rule[0])


@RequireLogin()
def post(request, testplan_id):
    """
    Create a new rule within a testplan based on testplan_id.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("only POST supported")

    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")

    if 'id' in new:  # Don't allow the user to shoot themselves in the foot providing dubious id
        del new['id']

    rule = rule_model.validate(new)
    if rule is None:
        return HttpResponseBadRequest("invalid rule")

    dbc = db_model.connect()
    try:
        testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
    except InvalidId:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)
    if testplan is None:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)

    if 'rules' in testplan:
        testplan['rules'].append(rule)
    else:
        testplan['rules'] = [rule]

    dbc.testplan.save(testplan)
    r = JsonResponse({"id": rule['id']}, status=200)
    r['location'] = "/api/testplan/%s/rule/%s" % (testplan_id, rule['id'])
    logger.info("rule '%s' within testplan '%s' created by '%s'" % (rule['id'], testplan_id, request.user['username']))
    return r


@RequireLogin()
def put(request, testplan_id, rule_id):
    """
    Update existing test plan based on testplan_id.
    """

    dbc = db_model.connect()
    try:
        testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
    except InvalidId:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)
    if testplan is None:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)

    for ri in range(0, len(testplan['rules'])):
        if testplan['rules'][ri]['id'] == rule_id:
            rule = testplan['rules'][ri]
            break

    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")

    rule.update(new)
    rule = rule_model.validate(rule)
    if rule is None:
        return HttpResponseBadRequest("invalid rule")

    testplan['rules'][ri] = rule

    dbc.testplan.save(testplan)
    r = HttpResponse(status=200)
    r['location'] = "/api/testplan/%s/rule/%s" % (testplan_id, rule['id'])
    logger.info("rule '%s' within testplan '%s' updated by '%s'" % (rule['id'], testplan_id, request.user['username']))
    return r


@RequireLogin()
def delete(request, testplan_id, rule_id):
    """
    Delete test plan based on testplan_id.
    """
    dbc = db_model.connect()
    try:
        testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
    except InvalidId:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)
    if testplan is None:
        return HttpResponseNotFound("testplan '%s' not found" % testplan_id)

    for i in range(0, len(testplan['rules'])):
        if testplan['rules'][i]['id'] == rule_id:
            del testplan['rules'][i]
            break

    dbc.testplan.save(testplan)
    logger.info("rule '%s' within testplan '%s' deleted by '%s'" % (rule_id, testplan_id, request.user['username']))
    return HttpResponse()
