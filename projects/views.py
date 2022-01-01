from django.shortcuts import render, get_object_or_404
from .models import Project

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    return render(request, "projects/projects.html", {"projects": projects})


def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project.html", {"project": project})