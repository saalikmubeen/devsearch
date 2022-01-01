from django.urls import path
from . import views

urlpatterns = [
    path("create-project", views.create_project, name="create-project"),
    path("update-project/<str:pk>", views.update_project, name="update-project"),
    path("", views.projects, name="projects"),
    path("<str:pk>", views.project, name="project")
]
