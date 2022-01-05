from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, CustomPasswordChangeForm
from .models import Profile, Skill
from .utils import search_profiles, paginate_profiles

# Create your views here.


def index(request):
    profiles, search_query = search_profiles(request)
    
    page_obj, custom_range, total_pages = paginate_profiles(request, profiles)
    
    return render(request, 'users/index.html', {"profiles": page_obj, "search_query": search_query, 
                                "page_range": custom_range, "total_pages": total_pages})

def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    
    other_skills = profile.skill_set.filter(description = "") # Get all skills that have no description
    top_skills = profile.skill_set.exclude(description__exact="") # Get all skills that have a description
    
    return render(request, 'users/user-profile.html', {"profile": profile, "other_skills": other_skills, "top_skills": top_skills})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    redirect_url = request.GET.get('next')
    
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
            return redirect(redirect_url if redirect_url else "account")
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


@login_required(login_url='login')
def update_skill(request, pk):
    skill = Skill.objects.get(pk=pk)
    
    if skill.owner.id != request.user.profile.id:
        raise PermissionError("You do not have permission to edit this skill")
    
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect("account")

    return render(request, 'users/skill_form.html', {"form": form})


@login_required(login_url='login')
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if skill.owner.id != request.user.profile.id:
        raise PermissionError("You do not have permission to edit this skill")
    
    if request.method == "POST":
        skill.delete()
        return redirect("account")
    
    return render(request, 'users/delete_skill.html', {"skill": skill})


@login_required(login_url='login')
def change_password(request):
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your Password has been changed successfully!')
            return redirect('account')
    else:
        form = CustomPasswordChangeForm(user=request.user)
        # update_session_auth_hash makes the user to be logged in after
        # user changes password, otherwise changing passwords logouts
        # the user by default.
    context = {'form': form}
    return render(request, 'users/change_password.html', context)

@login_required(login_url='login')
def inbox(request):
    received_messages = request.user.profile.received_messages.all()
    unread_messages = received_messages.filter(is_read=False).count()
    return render(request, 'users/inbox.html', {"received_messages": received_messages, "unread_messages": unread_messages})

@login_required(login_url='login')
def message(request, pk):
    message = request.user.profile.received_messages.get(pk=pk)
    message.is_read = True
    message.save()
    return render(request, 'users/message.html', {"message": message})