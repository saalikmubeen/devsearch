from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the users index.")


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, 'users/login.html')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            
            messages.success(request, 'User registered successfully!')
            
            login(request, user)
            return redirect("home")
        
        else:
            messages.error(request, 'An error has occurred during registration')
            
    return render(request, 'users/register.html', {"form": form})


def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")