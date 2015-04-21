import logging
from django.http import JsonResponse, HttpResponse
from api.models import db_model
from api.models.auth import RequireLogin
import re

logger = logging.getLogger(__name__)


@RequireLogin(role='admin')
def get(request):
    """
    Retrieve logs, limited by start/limit query string parameters.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    if 'start' in request.REQUEST:
        start = int(request.REQUEST['start'])
    else:
        start = 0

    if 'limit' in request.REQUEST:
        limit = int(request.REQUEST['limit'])
    else:
        limit = 1000

    query = {}
    if 'component' in request.REQUEST:
        regx = re.compile(r'^' + request.REQUEST['component'] + r'.*')
        query['name'] = regx

    if 'levels' in request.REQUEST and request.REQUEST['levels']:
        levels = request.REQUEST['levels'].split(',')
        query['level'] = {"$in": levels}

    dbc = db_model.connect()
    logs = [l for l in dbc.log.find(query, {"_id": 0})]
    logs.reverse()
    return JsonResponse({"log": logs[start:(start+limit)], "matchedEntries": dbc.log.find(query).count()})


def get_stats(request):
    """
    Retrieve log statistics.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    dbc = db_model.connect()
    component_names = dbc.log.distinct("name")
    levels = dbc.log.distinct("level")
    log_count = dbc.log.count()
    return JsonResponse({"entries": log_count, "components": component_names, "levels": levels})