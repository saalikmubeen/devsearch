from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import ProjectSerializer, ProfileSerializer
from projects.models import Project, Review


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
    

@api_view(["GET"])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_account(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vote_project(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data # {"value": "up"} or {"value": "down"}
    
    if project.owner.id == user.id:
        return Response({"error": "You cannot vote on your own project."})
    
    review, created = Review.objects.get_or_create(project=project, owner=user)
    review.value = data["value"]
    review.save()
    
    project.count_votes()
    
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)