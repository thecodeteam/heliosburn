from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from bson import ObjectId
from pymongo.helpers import DuplicateKeyError
from api.models.auth import RequireLogin
from api.models import rule_model
import json
from datetime import datetime
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
def get(request, rule_id=None):
    """
    Retrieve rule based on rule_id.
    """
    if rule_id is None:
        return get_all_rules()
    dbc = db_model.connect()
    try:
        rule = dbc.rule.find_one({"_id": ObjectId(rule_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if rule is None:
        return HttpResponseNotFound()
    else:
        rule['id'] = str(rule.pop('_id'))
        return JsonResponse(rule)


def get_all_rules():
    """
    Retrieve all rules.
    """
    dbc = db_model.connect()
    rules = [r for r in dbc.rule.find()]
    for rule in rules:
        rule['id'] = str(rule.pop('_id'))
    return JsonResponse({"rules": rules})


@RequireLogin()
def post(request):
    """
    Create new rule.
    """

    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    rule = rule_model.validate(new)
    if rule is None:
        return HttpResponseBadRequest("invalid rule")
    else:
        dbc = db_model.connect()
        rule['createdAt'] = datetime.isoformat(datetime.now())
        rule['updatedAt'] = datetime.isoformat(datetime.now())
        rule_id = str(dbc.rule.save(rule))
        r = JsonResponse({"id": rule_id})
        r['location'] = "/api/rule/%s" % rule_id
        logger.info("rule '%s' created by '%s'" % (rule_id, request.user['username']))
        return r

@RequireLogin()
def put(request, rule_id):
    """
    Update existing rule based on rule_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    try:
        rule = dbc.rule.find_one({"_id": ObjectId(rule_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if rule is None:
        return HttpResponseNotFound()
    else:
        in_json['createdAt'] = rule['createdAt']
        rule = rule_model.validate(in_json)
        if rule is None:
            return HttpResponseBadRequest("invalid rule")
        else:

            rule['_id'] = ObjectId(rule_id)
            rule['updatedAt'] = datetime.isoformat(datetime.now())
            dbc.rule.save(rule)
            r = JsonResponse({"id": rule_id})
            r['location'] = "/api/rule/%s" % rule_id
            logger.info("rule '%s' updated by '%s'" % (rule_id, request.user['username']))
            return r



@RequireLogin()
def delete(request, rule_id):
    """
    Delete rule based on rule_id.
    """
    dbc = db_model.connect()
    try:
        rule = dbc.rule.find_one({'_id': ObjectId(rule_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if rule is None:
        return HttpResponseNotFound()
    else:
        dbc.rule.remove({"_id": ObjectId(rule_id)})
        logger.info("rule '%s' deleted by '%s'" % (rule_id, request.user['username']))
        return HttpResponse()