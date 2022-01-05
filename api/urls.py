from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_routes, name="get-routes"),
    path("projects/", views.get_projects, name="get-projects"),
]
