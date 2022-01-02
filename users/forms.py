from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


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