from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects

# Create your views here.

def projects(request):
    print(request.path)
    
    projects, search_query = search_projects(request)
    
    page_obj, custom_range, total_pages = paginate_projects(request, projects)
    
    return render(request, "projects/projects.html", {"projects": page_obj, "page_range": custom_range,
                                                "total_pages": total_pages, "search_query": search_query})


def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ReviewForm()
    
    reviews = project.review_set.all()
    
    already_reviewed = False
    if request.user.is_authenticated:
        already_reviewed = any([review.owner.id == request.user.profile.id for review in reviews])
        
        #OR
        # already_reviewed = request.user.profile.id in project.reviewers()
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()
            project.count_votes()
            
            messages.success(
                request, 'Your review was successfully submitted!')
            
            return redirect(reverse("project", kwargs={"pk": project.id}))
    
    return render(request, "projects/project.html", {"project": project, "form": form, "reviews": reviews, "already_reviewed": already_reviewed})


@login_required(login_url="login")
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
            
            form.save_m2m()
            
            for tag in newtags:
                new_tag = Tag.objects.get_or_create(name=tag) # new_tag = (tag, created) -> created = Boolean
                project.tags.add(new_tag[0])
                project.save()
            return redirect("account")
        
    return render(request, "projects/project_form.html", {"form": form})


@login_required(login_url="login")
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
            
            form.save_m2m()
            
            newtags = request.POST.get('newtags').split(',')
            
            for tag in newtags:
                if tag != "":
                    new_tag = Tag.objects.get_or_create(name=tag)
                    project.tags.add(new_tag[0])
                    # project.save()
            return redirect("account")
        
    return render(request, "projects/project_form.html", {"form": form})


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = get_object_or_404(Project, pk=pk)
    
    if project.owner.id != profile.id:
        raise PermissionError(
            "You do not have permission to delete this project.")
    
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'project': project}
    return render(request, 'projects/delete_project.html', context)
