import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models.auth import RequireLogin
from api.models import redis_wrapper


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
    except TypeError as e:
            print e
            return HttpResponseBadRequest("unknown method")


@RequireLogin
def get(request):
    """
    Retrieve traffic from redis backend.
    """
    r = redis_wrapper.init_redis()

    key = 'token:%s' % (request.token_string,)
    last_score = r.hget(key, 'last_score')

    if last_score:
        last_score = int(last_score)
    else:
        # get the last score from Redis
        traffic = r.zrevrange('heliosburn.traffic', 0, 0, withscores=True)
        last_score = int(traffic[0][1])+1 if len(traffic) > 0 else 0

    traffic = r.zrangebyscore('heliosburn.traffic', last_score, '+inf', withscores=True)

    requests = []
    for message in traffic:
        request = json.loads(message[0])
        requests.append(request)
        score = int(message[1])

        # update the last_time to obtain new traffic the next time
        if score > last_score:
            last_score = score + 1  # increment by 1 to avoid getting the last request again

    # update last score of the user
    r.hset(key, 'last_score', last_score)

    r = {
        "count": len(requests),
        "requests": requests
        }
    return JsonResponse(r)

@RequireLogin
def post(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r

@RequireLogin
def put(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r
        

@RequireLogin
def delete(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r

