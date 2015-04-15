from django.http import JsonResponse, HttpResponse
from api.models import db_model
from api.models.auth import RequireLogin
from api.models.redis_wrapper import logger


@RequireLogin(role='admin')
def get(request):
    """
    Retrieve logs, limited by start/offset query string parameters.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    if 'start' in request.REQUEST:
        start = int(request.REQUEST['start'])
    else:
        start = 0

    if 'offset' in request.REQUEST:
        offset = int(request.REQUEST['offset'])
    else:
        offset = 100

    dbc = db_model.connect()
    logs = [l for l in dbc.log.find({}, {"_id": 0})]
    return JsonResponse({"log": logs[start:(start+offset)]})