from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from api.models.auth import RequireLogin
from api.models import rule_model
from pymongo.helpers import DuplicateKeyError
from bson import ObjectId
import json
from datetime import datetime


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
def get(request, testplan_id=None):
    """
    Retrieve test plan based on testplan_id.
    """
    if testplan_id is None:
        return get_all_testplans()

    dbc = db_model.connect()
    testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)}, {'_id': 0})
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        testplan['id'] = testplan_id  # Replace ObjectId with str version
        return JsonResponse(testplan, status=200)


def get_all_testplans():
    """
    Retrieve all test plans.
    """
    dbc = db_model.connect()
    testplans = [t for t in dbc.testplan.find()]
    for t in testplans:
        # Find and append any sessions within each testplan
        sessions = [s for s in dbc.session.find({"testplan": t['_id']})]

        for s in sessions:  # Translate _id to id
            s['id'] = str(s.pop('_id'))
        t['id'] = str(t.pop('_id'))

    return JsonResponse({"testplans": testplans}, status=200)


@RequireLogin()
def post(request):
    """
    Create new test plan.
    """
    try:
        new = json.loads(request.body)
        assert "name" in new
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")

    if 'rules' in new:
        new['rules'] = [rule_model.validate(rule) for rule in new['rules']]
        if None in new['rules']:  # Invalid rules are re-assigned to None
            return HttpResponse("invalid rule(s) provided")

    dbc = db_model.connect()
    testplan = dbc.testplan.find_one({"name": new['name']})
    if testplan is not None:
        return HttpResponse("testplan named '%s' already exists" % new['name'])

    new['createdAt'] = datetime.isoformat(datetime.now())
    new['updatedAt'] = datetime.isoformat(datetime.now())
    testplan_id = str(dbc.testplan.save(new))
    r = JsonResponse({"id": testplan_id}, status=200)
    r['location'] = "/api/testplan/%s" % testplan_id
    return r


@RequireLogin()
def put(request, testplan_id):
    """
    Update existing test plan based on testplan_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        if "name" in in_json:
            testplan['name'] = in_json['name']
        if "description" in in_json:
            testplan['description'] = in_json['description']
        if "latencyEnabled" in in_json:
            testplan['latencyEnabled'] = in_json['latencyEnabled']
        if "clientLatency" in in_json:
            testplan['clientLatency'] = in_json['clientLatency']
        if "serverLatency" in in_json:
            testplan['serverLatency'] = in_json['serverLatency']
        if "rules" in in_json:
            testplan['rules'] = [rule_model.validate(rule) for rule in in_json['rules']]
            if None in in_json['rules']:
                return HttpResponse("invalid rule(s) provided")
        try:
            testplan['updatedAt'] = datetime.isoformat(datetime.now())
            dbc.testplan.save(testplan)
        except DuplicateKeyError:
            return HttpResponseBadRequest("testplan named '%s' already exists" % in_json['name'])
        return HttpResponse(status=200)


@RequireLogin()
def delete(request, testplan_id):
    """
    Delete test plan based on testplan_id.
    """
    dbc = db_model.connect()
    testplan = dbc.testplan.find_one({"_id": ObjectId(testplan_id)})
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        dbc.testplan.remove({"_id": ObjectId(testplan_id)})
        return HttpResponse(status=200)
