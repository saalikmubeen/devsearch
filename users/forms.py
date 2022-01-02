from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]
        labels = {
            "first_name": "Name"
        }
        
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input"
            })
        # print(self.fields)
        
    
class CustomPasswordChangeForm(PasswordChangeForm):
        
        class Meta:
            model = User
            fields = ["old_password", "new_password1", "new_password2"]
            labels = {
                "old_password": "Current Password",
                "new_password1": "New Password",
                "new_password2": "Confirm New Password"
            }
            
        
        def __init__(self, *args, **kwargs):
            super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
            
            for field in self.fields.values():
                field.widget.attrs.update({
                    "class": "input"
                })

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "bio": "Bio",
            "location": "Location",
            "birth_date": "Birth Date",
            "profile_pic": "Profile Picture"
        }
        
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input"
            })
            

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        exclude = ["owner"]
        
        
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input"
            })