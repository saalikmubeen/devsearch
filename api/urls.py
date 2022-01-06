from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("", views.get_routes, name="get-routes"),
    path("projects/", views.get_projects, name="get-projects"),
    path("projects/<str:pk>", views.get_project, name="get-project"),
    path("projects/<str:pk>/vote/", views.vote_project, name="vote-project"),
    
    path("users/account", views.get_user_account, name="user-account"),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
