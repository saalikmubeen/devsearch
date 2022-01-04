from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_routes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    
    return Response(routes)
    
    # return JsonResponse(routes, safe=False)
    