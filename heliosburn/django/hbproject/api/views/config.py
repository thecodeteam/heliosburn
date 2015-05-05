from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from hbproject import settings


def get(request):
    """
    Return settings.py values
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    if ("api_key" not in request.GET) or (request.GET["api_key"] != settings.API_KEY):
        return HttpResponse(status=401)

    internal_config = {
        "redis": {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "db": settings.REDIS_DB
        },
        "mongodb": {
            "host": settings.MONGODB_HOST,
            "port": settings.MONGODB_PORT,
            "db": settings.MONGODB_DATABASE
        }
    }
    return JsonResponse({"config": internal_config})
