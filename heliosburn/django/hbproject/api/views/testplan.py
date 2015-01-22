from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from api.models.auth import RequireLogin
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
            r = JsonResponse({"error": "arguments mismatch"})
            r.status_code = 400
            return r


def get(request, testplan_id=None):
    """Retrieve a test plan."""
    if testplan_id is None:
        return get_all_testplans()

    dbsession = db_model.init_db()
    testplan = dbsession.query(db_model.TestPlan).filter_by(id=testplan_id).first()
    if testplan is None:
        r = JsonResponse({})
        r.status_code = 404
        return r
    else:
        r = JsonResponse({
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
        r.status_code = 200
        return r


def get_all_testplans():
    """Retrieve all test plans."""
    dbsession = db_model.init_db()
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
    r = JsonResponse({"testplans": all_testplans})
    r.status_code = 200
    return r


def post(request):
    """Create a new test plan."""
    try:
        new = json.loads(request.body)
        assert "name" in new
    except ValueError:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r
    except AssertionError:
        r = JsonResponse({"error": "argument mismatch"})
        r.status_code = 400
        return r

    dbsession = db_model.init_db()
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
    r = JsonResponse({})
    r.status_code = 204
    return r


def put(request, testplan_id):
    """Update existing test plan."""
    try:
        in_json = json.loads(request.body)
    except ValueError:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    dbsession = db_model.init_db()
    testplan = db_model.query(db_model.TestPlan).filter_by(id=testplan_id).first()
    if testplan is None:
        r = JsonResponse({})
        r.status_code = 404
        return r
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
            r = JsonResponse({"error": "constraint violated"})
            r.status_code = 409
            return r
        r = JsonResponse({})
        r.status_code = 204
        return r


def delete(request, testplan_id):
    """Delete existing test plan."""

