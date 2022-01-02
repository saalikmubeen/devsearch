from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginUser, name="login"),
    path('register', views.registerUser, name="register"),
    path('logout', views.logoutUser, name="logout"),
    
    path("", views.index, name="home"),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('account/', views.user_account, name="account"),
]
