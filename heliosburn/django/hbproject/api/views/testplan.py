from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from api import models
import json

from IPython.core.debugger import Tracer

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
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, username=None):
    """Retrieve a test plan."""
    pass


def post(request):
    """Create a new test plan."""
    pass

def put(request, testplan_id):
    """Update existing test plan."""
    pass

def delete(request, testplan_id):
    """Delete existing test plan."""
    pass
