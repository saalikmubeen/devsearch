from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    return render(request, "projects/projects.html", {"projects": projects})


def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project.html", {"project": project})

@login_required
def create_project(request):
    user_profile = request.user.profile
    form = ProjectForm()
    
    if request.method == "POST":
        newtags = request.POST.getlist('newtags')[0].split(',')
        
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user_profile
            project.save()
            
            for tag in newtags:
                new_tag = Tag.objects.get_or_create(name=tag)
                project.tags.add(new_tag[0])
            return redirect("projects")
        
    return render(request, "projects/project_form.html", {"form": form})


@login_required
def update_project(request, pk):
    profile = request.user.profile
    project = get_object_or_404(Project, pk=pk)
    if project.owner.id != profile.id:
        raise PermissionError(
            "You do not have permission to edit this project.")
        
    form = ProjectForm(instance=project)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            
            newtags = request.POST.get('newtags').split(',')
            
            for tag in newtags:
                new_tag = Tag.objects.get_or_create(name=tag)
                project.tags.add(new_tag[0])
            
            return redirect("projects")
        
    return render(request, "projects/project_form.html", {"form": form})