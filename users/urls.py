from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('logout', views.logoutUser, name="logout"),
    
    path("", views.index, name="home"),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('account/', views.user_account, name="account"),
    path('change-password/', views.change_password, name="change-password"),
    
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path('create-skill/', views.create_skill, name="create-skill"),
    path('update-skill/<str:pk>/', views.update_skill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.delete_skill, name="delete-skill"),
]
