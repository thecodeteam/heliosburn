from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from api import models
import inspect

#from IPython.core.debugger import Tracer

@csrf_exempt
def rest(request):
    """
    Calls python function corresponding with HTTP METHOD name. 
    Calls with incomplete arguments will return HTTP 400 with a description and argument list.
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

    # Call appropriate REST function, passing the conents of request.GET as keyword paremeters
    # Calls that raise a TypeError will return a serialized description and arg list to the client
    try:
        return rest_function(request, **request.GET)
    except TypeError:
            required_arguments = inspect.getargspec(rest_function).args
            required_arguments.remove('request') # Remove the request object, client doesn't need to see this
            description = inspect.getdoc(rest_function)
            r = JsonResponse({"description": description, "arguments": required_arguments})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, name):
    """Retrieve a test_plan."""
    #TODO
    return JsonResponse({"todo": "todo"})


def post(request, name, description, testplan_id, user_id):
    """Create a new test_plan."""
    #TODO
    return JsonResponse({"todo": "todo"})


def put(request):
    """Update existing test_plan."""
    #TODO
    return JsonResponse({"todo": "todo"})
        

def delete(request):
    """Delete existing test_plan."""
    #TODO
    return JsonResponse({"todo": "todo"})
