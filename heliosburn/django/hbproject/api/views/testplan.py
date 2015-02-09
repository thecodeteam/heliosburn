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
def get(request, testplan_id=None, dbsession=None):
    """
    Retrieve test plan based on testplan_id.
    """
    if testplan_id is None:
        return get_all_testplans(dbsession=dbsession)

    testplan = dbsession.query(db_model.TestPlan).filter_by(id=testplan_id).first()
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        return JsonResponse({
            'id': testplan.id,
            'name': testplan.name,
            'description': testplan.description,
            'created_at': testplan.created_at,
            'updated_at': testplan.updated_at,
            'latency_enabled': testplan.latency_enabled,
            'client_latency': testplan.client_latency,
            'server_latency': testplan.server_latency,
            'rules': testplan.rules,
            }, status=200)


def get_all_testplans(dbsession=None):  # TODO: this should require admin
    """
    Retrieve all test plans.
    """
    testplans = dbsession.query(db_model.TestPlan).all()
    all_testplans = list()
    for testplan in testplans:
        all_testplans.append({
            'id': testplan.id,
            'name': testplan.name,
            'description': testplan.description,
            'created_at': testplan.created_at,
            'updated_at': testplan.updated_at,
            'latency_enabled': testplan.latency_enabled,
            'client_latency': testplan.client_latency,
            'server_latency': testplan.server_latency,
            'rules': testplan.rules,
            })
    return JsonResponse({"testplans": all_testplans}, status=200)


@RequireLogin()
@RequireDB()
def post(request, dbsession=None):
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

    testplan = db_model.TestPlan(name=new['name'])
    if "description" in new:
        testplan.description = new['description']
    if "latency_enabled" in new:
        testplan.latency_enabled = new['latency_enabled']
    if "client_latency" in new:
        testplan.client_latency = new['client_latency']
    if "server_latency" in new:
        testplan.server_latency = new['server_latency']

    dbsession.add(testplan)
    dbsession.commit()
    return JsonResponse({"id": testplan.id}, status=200)


@RequireLogin()
@RequireDB()
def put(request, testplan_id, dbsession=None):
    """
    Update existing test plan based on testplan_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    testplan = dbsession.query(db_model.TestPlan).filter_by(id=testplan_id).first()
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        if "name" in in_json:
            testplan.name = in_json['name']
        if "description" in in_json:
            testplan.description = in_json['description']
        if "latency_enabled" in in_json:
            testplan.latency_enabled = in_json['latency_enabled']
        if "client_latency" in in_json:
            testplan.client_latency = in_json['client_latency']
        if "server_latency" in in_json:
            testplan.server_latency = in_json['server_latency']
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)


@RequireLogin()
@RequireDB()
def delete(request, testplan_id, dbsession=None):
    """
    Delete test plan based on testplan_id.
    """
    testplan = dbsession.query(db_model.TestPlan).filter_by(id=testplan_id).first()
    if testplan is None:
        return HttpResponseNotFound("")
    else:
        dbsession.delete(testplan)
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("constraint violated")
        return HttpResponse(status=200)



