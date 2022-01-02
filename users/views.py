from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile

# Create your views here.


def index(request):
    profiles = Profile.objects.all()
    return render(request, 'users/index.html', {"profiles": profiles})

def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    
    other_skills = profile.skill_set.filter(description = "") # Get all skills that have no description
    top_skills = profile.skill_set.exclude(description__exact="") # Get all skills that have a description
    
    return render(request, 'users/user-profile.html', {"profile": profile, "other_skills": other_skills, "top_skills": top_skills})


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

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    return render(request, 'users/account.html', {"profile": profile})


@login_required(login_url='login')
def edit_profile(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("account")
        
    return render(request, 'users/edit_profile.html', {"form": form})


@login_required(login_url='login')
def create_skill(request):
    form = SkillForm()
    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect("account")
        
    return render(request, 'users/skill_form.html', {"form": form})