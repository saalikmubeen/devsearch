from django.urls import path
from . import views

urlpatterns = [
    path("create-project", views.project_form, name="project-form"),
    path("", views.projects, name="projects"),
    path("<str:pk>", views.project, name="project")
]
